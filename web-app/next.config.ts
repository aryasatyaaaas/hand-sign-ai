import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  /* config options here */
  transpilePackages: ['@mediapipe/hands', '@mediapipe/camera_utils', '@mediapipe/drawing_utils'],
};

export default nextConfig;
