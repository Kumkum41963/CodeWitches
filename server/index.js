import express from "express";
import * as dotenv from "dotenv";
import cors from "cors";
import mongoose from "mongoose";
import UserRoutes from "./routes/User.js";

// Load environment variables
dotenv.config();

const app = express();
app.use(cors());
app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true }));

// Routes
app.use("/api/user/", UserRoutes);

// Error handler middleware
app.use((err, req, res, next) => {
  const status = err.status || 500;
  const message = err.message || "Something went wrong";
  return res.status(status).json({
    success: false,
    status,
    message,
  });
});

// Default route
app.get("/", async (req, res) => {
  res.status(200).json({
    message: "Hello developers from GFG",
  });
});

// MongoDB connection
const connectDB = async () => {
  try {
    mongoose.set("strictQuery", true);

    console.log("Connecting to MongoDB...");
    await mongoose.connect(process.env.MONGODB_URL);
    console.log("Connected to MongoDB");
  } catch (error) {
    console.error("Failed to connect to MongoDB");
    console.error(error);
    process.exit(1); // Exit process with failure
  }
};

// Start server
const startServer = async () => {
  try {
    await connectDB();
    app.listen(8080, () => console.log("Server started on port 8080"));
  } catch (error) {
    console.error("Failed to start the server");
    console.error(error);
  }
};

startServer();
