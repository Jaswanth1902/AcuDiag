/**
 * AcuDiag Direct WhatsApp Device Gateway
 * Uses WhiskeySockets/Baileys to link directly to WhatsApp with ZERO third-party intermediaries (No Twilio).
 * Forwards all incoming WhatsApp messages & voice notes to AcuDiag Python Gateway -> Pine Labs AgenticOrg.
 */

const { default: makeWASocket, useMultiFileAuthState, DisconnectReason, downloadMediaMessage } = require('@whiskeysockets/baileys');
const qrcode = require('qrcode-terminal');
const fs = require('fs');
const path = require('path');
const http = require('http');

const ACUDIAG_WEBHOOK_URL = 'http://127.0.0.1:8000/api/whatsapp/webhook';

async function startWhatsAppGateway() {
    const authDir = path.join(__dirname, 'auth_session');
    const { state, saveCreds } = await useMultiFileAuthState(authDir);

    console.log('\n======================================================');
    console.log('⚡ Starting AcuDiag Direct WhatsApp Gateway (Zero Third Parties)');
    console.log('======================================================\n');

    let pinoLogger;
    try {
        const pino = require('pino');
        pinoLogger = pino({ level: 'silent' });
    } catch (e) {
        // fallback
    }

    const sock = makeWASocket({
        auth: state,
        logger: pinoLogger,
        browser: ['AcuDiag Orchestrator', 'Chrome', '1.0.0']
    });

    sock.ev.on('creds.update', saveCreds);

    sock.ev.on('connection.update', (update) => {
        const { connection, lastDisconnect, qr } = update;
        if (qr) {
            console.log('\n================== SCAN WITH WHATSAPP ==================');
            qrcode.generate(qr, { small: true });
            console.log('👉 WhatsApp (phone) -> Settings -> Linked Devices -> Link a Device\n');
        }
        if (connection === 'close') {
            const shouldReconnect = lastDisconnect?.error?.output?.statusCode !== DisconnectReason.loggedOut;
            console.log('Connection closed, reconnecting:', shouldReconnect);
            if (shouldReconnect) {
                startWhatsAppGateway();
            }
        } else if (connection === 'open') {
            console.log('\n✅ WHATSAPP CONNECTED DIRECTLY! Ready to receive messages & voice notes from your phone!\n');
            console.log('👉 Send a message or voice note to this number/chat on WhatsApp to test!\n');
        }
    });

    sock.ev.on('messages.upsert', async (m) => {
        if (!m.messages || !m.messages[0]) return;
        const msg = m.messages[0];

        // Skip messages that have no content or are protocol syncs
        if (!msg.message) return;

        const remoteJid = msg.key.remoteJid;
        const sender = msg.pushName || remoteJid;
        
        let bodyText = msg.message.conversation 
            || msg.message.extendedTextMessage?.text 
            || msg.message.imageMessage?.caption 
            || '';

        let audioFile = '';

        // Check if voice note or audio
        if (msg.message.audioMessage) {
            console.log(`🎙️ Received voice note from ${sender}... Downloading audio...`);
            try {
                const buffer = await downloadMediaMessage(msg, 'buffer', {});
                const tempAudioPath = path.join(__dirname, `voice_${Date.now()}.ogg`);
                fs.writeFileSync(tempAudioPath, buffer);
                audioFile = tempAudioPath;
                console.log(`   Saved voice note: ${audioFile} (${buffer.length} bytes)`);
            } catch (err) {
                console.error('Failed to download voice note:', err);
            }
        } else if (bodyText) {
            console.log(`📩 Received WhatsApp message from ${sender}: "${bodyText}"`);
        } else {
            return;
        }

        // Construct Meta-compliant payload for AcuDiag FastAPI bridge
        const payload = {
            entry: [{
                changes: [{
                    value: {
                        messages: [{
                            from: remoteJid,
                            type: audioFile ? 'audio' : 'text',
                            text: { body: bodyText },
                            audio: { id: audioFile }
                        }]
                    }
                }]
            }]
        };

        console.log('📡 Dispatching directly to AcuDiag & Pine Labs AgenticOrg...');
        try {
            const postData = JSON.stringify(payload);
            const req = http.request(ACUDIAG_WEBHOOK_URL, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Content-Length': Buffer.byteLength(postData)
                }
            }, (res) => {
                let respBody = '';
                res.on('data', chunk => respBody += chunk);
                res.on('end', async () => {
                    try {
                        const data = JSON.parse(respBody);
                        const reply = data.reply || 'Diagnosing appliance...';
                        console.log('💬 Sending verified diagnosis reply to WhatsApp...');
                        await sock.sendMessage(remoteJid, { text: reply });
                        console.log('✅ Reply sent successfully to WhatsApp!');

                        // Clean up audio file if created
                        if (audioFile && fs.existsSync(audioFile)) {
                            fs.unlinkSync(audioFile);
                        }
                    } catch (e) {
                        console.error('Error parsing AcuDiag response:', e, respBody);
                    }
                });
            });

            req.on('error', (e) => {
                console.error('Error connecting to AcuDiag bridge:', e.message);
            });

            req.write(postData);
            req.end();
        } catch (err) {
            console.error('Dispatch error:', err);
        }
    });
}

startWhatsAppGateway().catch(console.error);
