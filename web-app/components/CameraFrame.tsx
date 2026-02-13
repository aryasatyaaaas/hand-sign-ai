'use client';

import React, { useRef, useEffect, useState, useCallback } from 'react';
import Webcam from 'react-webcam';
import Script from 'next/script';
import * as tf from '@tensorflow/tfjs';

/* eslint-disable @typescript-eslint/no-explicit-any */

interface CameraFrameProps {
    onPrediction: (prediction: string) => void;
}

const CameraFrame: React.FC<CameraFrameProps> = ({ onPrediction }) => {
    const webcamRef = useRef<Webcam>(null);
    const canvasRef = useRef<HTMLCanvasElement>(null);
    const [cameraActive, setCameraActive] = useState(false);
    const [scriptsLoaded, setScriptsLoaded] = useState(false);
    const [model, setModel] = useState<tf.LayersModel | null>(null);
    const [classes, setClasses] = useState<string[]>([]);
    const handsRef = useRef<any>(null);
    const cameraRef = useRef<any>(null);

    const onResults = useCallback(async (results: any) => {
        if (!canvasRef.current || !webcamRef.current?.video) return;

        const canvasCtx = canvasRef.current.getContext('2d');
        if (!canvasCtx) return;

        const videoWidth = webcamRef.current.video.videoWidth;
        const videoHeight = webcamRef.current.video.videoHeight;

        canvasRef.current.width = videoWidth;
        canvasRef.current.height = videoHeight;

        canvasCtx.save();
        canvasCtx.clearRect(0, 0, canvasRef.current.width, canvasRef.current.height);
        canvasCtx.drawImage(results.image, 0, 0, canvasRef.current.width, canvasRef.current.height);

        if (results.multiHandLandmarks) {
            for (const landmarks of results.multiHandLandmarks) {
                if ((window as any).drawConnectors) {
                    (window as any).drawConnectors(canvasCtx, landmarks, (window as any).HAND_CONNECTIONS, { color: '#00FF00', lineWidth: 5 });
                }
                if ((window as any).drawLandmarks) {
                    (window as any).drawLandmarks(canvasCtx, landmarks, { color: '#FF0000', lineWidth: 2 });
                }

                // Prediction Logic
                if (model && classes.length > 0) {
                    console.log('Predicting...'); // Debug log
                    const inputData: number[] = [];
                    for (const landmark of landmarks) {
                        inputData.push(landmark.x, landmark.y, landmark.z);
                    }

                    const inputTensor = tf.tensor2d([inputData], [1, 63]);
                    try {
                        const prediction = model.predict(inputTensor) as tf.Tensor;
                        const classIndex = prediction.argMax(1).dataSync()[0];
                        const predictedLabel = classes[classIndex];
                        onPrediction(predictedLabel);
                        console.log('Prediction Result:', predictedLabel);
                    } catch (err) {
                        console.error("Prediction error:", err);
                    } finally {
                        inputTensor.dispose();
                    }
                } else {
                    // Throttle logs to avoid spam
                    if (Math.random() < 0.01) {
                        console.log('Model or classes not loaded yet. Model:', !!model, 'Classes:', classes.length);
                    }
                }
            }
        }
        canvasCtx.restore();
    }, [onPrediction, model, classes]);

    const [modelStatus, setModelStatus] = useState<string>('Initializing...');
    const [modelError, setModelError] = useState<string | null>(null);

    useEffect(() => {
        const loadResources = async () => {
            try {
                setModelStatus('Setting up TensorFlow backend...');
                await tf.setBackend('webgl');
                await tf.ready();
                console.log('TF Backend ready:', tf.getBackend());

                setModelStatus('Loading model...');
                console.log('Loading model...');
                const loadedModel = await tf.loadLayersModel('/model/model.json');
                setModel(loadedModel);
                console.log('Model loaded successfully');

                setModelStatus('Loading classes...');
                console.log('Loading classes...');
                const response = await fetch('/model/classes.json');
                const loadedClasses = await response.json();
                setClasses(loadedClasses);
                console.log('Classes loaded:', loadedClasses);

                setModelStatus('Ready');
            } catch (error: any) {
                console.error('Failed to load model or classes:', error);
                setModelError(error.message || 'Unknown error loading model');
                setModelStatus('Error');
            }
        };

        loadResources();
    }, []);

    useEffect(() => {
        if (scriptsLoaded) {
            const Hands = (window as any).Hands;
            const hands = new Hands({
                locateFile: (file: string) => {
                    return `https://cdn.jsdelivr.net/npm/@mediapipe/hands/${file}`;
                },
            });

            hands.setOptions({
                maxNumHands: 1,
                modelComplexity: 1,
                minDetectionConfidence: 0.5,
                minTrackingConfidence: 0.5,
            });

            hands.onResults(onResults);
            handsRef.current = hands;

            return () => {
                hands.close();
            };
        }
    }, [scriptsLoaded, onResults]);

    const onUserMedia = useCallback(() => {
        if (webcamRef.current && webcamRef.current.video && handsRef.current && (window as any).Camera) {
            const Camera = (window as any).Camera;
            const camera = new Camera(webcamRef.current.video, {
                onFrame: async () => {
                    if (webcamRef.current?.video && handsRef.current) {
                        await handsRef.current.send({ image: webcamRef.current.video });
                    }
                },
                width: 640,
                height: 480
            });
            camera.start();
            cameraRef.current = camera;
            setCameraActive(true);
        }
    }, [scriptsLoaded]);

    return (
        <div className="relative rounded-2xl overflow-hidden shadow-2xl border-4 border-white/10">
            {/* Scripts ... */}
            <Script src="https://cdn.jsdelivr.net/npm/@mediapipe/camera_utils/camera_utils.js" strategy="lazyOnload" />
            <Script src="https://cdn.jsdelivr.net/npm/@mediapipe/control_utils/control_utils.js" strategy="lazyOnload" />
            <Script src="https://cdn.jsdelivr.net/npm/@mediapipe/drawing_utils/drawing_utils.js" strategy="lazyOnload" />
            <Script
                src="https://cdn.jsdelivr.net/npm/@mediapipe/hands/hands.js"
                strategy="lazyOnload"
                onLoad={() => setScriptsLoaded(true)}
            />

            <Webcam
                ref={webcamRef}
                className="hidden" // Hide the raw video, we draw on canvas
                width={640}
                height={480}
                screenshotFormat="image/jpeg"
                videoConstraints={{ facingMode: "user" }}
                onUserMedia={onUserMedia}
            />
            <canvas
                ref={canvasRef}
                className="w-full h-auto block bg-black/50"
            />

            {/* Loading / Status Overlay */}
            {(!cameraActive || modelStatus !== 'Ready') && (
                <div className="absolute inset-0 flex flex-col items-center justify-center bg-gray-900/90 text-white p-4 text-center">
                    <p className="text-xl font-bold mb-2">
                        {modelError ? "Error Loading AI" : "Starting Up..."}
                    </p>
                    <p className="text-sm text-gray-300">
                        Camera: {scriptsLoaded ? "Scripts Loaded" : "Loading Scripts..."}<br />
                        AI Status: {modelStatus}
                    </p>
                    {modelError && (
                        <div className="mt-4 p-2 bg-red-500/20 border border-red-500 text-red-100 rounded text-xs">
                            {modelError}
                        </div>
                    )}
                </div>
            )}
        </div>
    );
};


export default CameraFrame;
