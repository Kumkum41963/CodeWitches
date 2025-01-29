import express from 'express';
import cors from 'cors';
import { spawn } from 'child_process';
import fs from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';

const app = express();

const corsOptions = {
  origin: 'http://localhost:3000', // Specify your frontend URL
  methods: ['GET', 'POST', 'OPTIONS'], // Allow specific HTTP methods
  allowedHeaders: ['Content-Type', 'Authorization'], // Allow specific headers
  preflightContinue: false, // Do not pass the preflight request to the next middleware
  optionsSuccessStatus: 204, // Respond with status 204 for preflight request
};

app.use(cors(corsOptions));

app.use(express.json({ limit: '50mb' })); // Increase payload limit for large base64 strings

let frameCount = 0; // Initialize a counter to keep track of frames

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

// Process route to handle base64 frames
app.post('/process', async (req, res) => {
  console.log('Received POST request at /process');

  const { frame } = req.body;

  if (!frame) {
    console.error('No frame provided in the request body.');
    return res.status(400).json({ error: 'No frame provided' });
  }

  try {
    console.log('Frame received. Length:', frame.length);

    // Increment the frame counter
    frameCount += 1;

    // Create a unique temporary file name (e.g., frame1.txt, frame2.txt)
    const tempFilePath = path.join(__dirname, `frame${frameCount}.txt`);
    console.log(`Creating temporary file at: ${tempFilePath}`);
    fs.writeFileSync(tempFilePath, frame);

    console.log('Temporary file written successfully.');

    // Pass the path of the temporary file to the Python script
    console.log('Spawning Python process...');
    const pythonProcess = spawn('python', ['process_frame.py', '--frameFile', tempFilePath]);

    let processedData = '';

    // Capture Python script stdout
    pythonProcess.stdout.on('data', (data) => {
      console.log('Python stdout:', data.toString());
      processedData += data.toString();
    });

    // Capture Python script stderr
    pythonProcess.stderr.on('data', (data) => {
      console.error('Python stderr:', data.toString());
    });

    // Handle when Python process exits
    pythonProcess.on('close', (code) => {
      console.log(`Python process exited with code: ${code}`);

      // Clean up the temporary file after processing
      if (fs.existsSync(tempFilePath)) {
        console.log('Deleting temporary file...');
        fs.unlinkSync(tempFilePath);
        console.log('Temporary file deleted successfully.');
      } else {
        console.warn(`Temporary file ${tempFilePath} does not exist. Skipping deletion.`);
      }

      if (code === 0) {
        console.log('Python process completed successfully. Sending response.');
        res.json({ frame: processedData });
      } else {
        console.error('Python process failed.');
        res.status(500).json({ error: 'Failed to process frame' });
      }
    });
  } catch (err) {
    console.error('Error during frame processing:', err);
    res.status(500).json({ error: 'Error processing frame' });
  }
});

// Start the server
const PORT = 5000;
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
});