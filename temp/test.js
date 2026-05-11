import fs from 'fs';

const emailContent = fs.readFileSync('mail3.txt', 'utf-8');

const run = async () => {
    console.log('Running test.js');
    const res = await fetch('http://localhost:5000/api/email', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            recipient: 'nadunrz101@gmail.com',
            subject: 'Test Email',
            body: emailContent,
            language: 'en',
            mail_type: 'confirmation',
        }),
    });
    const data = await res.json();
    console.log('Response from /email:', data);
}

run();