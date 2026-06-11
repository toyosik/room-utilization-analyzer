import express, { Request, Response } from 'express';
import { exec } from 'child_process';
import * as path from 'path';

const app = express();
const PORT = 4000;

app.use(express.json());

// Main Endpoint to fetch real-time Capacity Reports
app.get('/api/reports/capacity', (req: Request, res: Response) => {
    const scriptPath = path.join(__dirname, 'analyzer.py');
    const databasePath = path.join(__dirname, 'scheduling.db');

    // Execute the Python analytical engine safely as a sub-process
    exec(`python3 ${scriptPath} ${databasePath}`, (error, stdout, stderr) => {
        if (error) {
            console.error(`Execution Error: ${error}`);
            return res.status(500).json({ error: "Internal processing engine failure." });
        }
        if (stderr) {
            console.error(`Engine Warning: ${stderr}`);
        }

        try {
            // Parse the stdout JSON payload returned from the Python engine
            const analyticalReport = JSON.parse(stdout);
            res.status(200).json(analyticalReport);
        } catch (parseError) {
            res.status(500).json({ error: "Failed to parse data processing payload." });
        }
    });
});

app.listen(PORT, () => {
    console.log(`[TypeScript Server] Analytical API streaming active on port ${PORT}`);
});
