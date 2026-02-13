'use client';

import { useState } from 'react';
import CameraFrame from '@/components/CameraFrame';
import { Sparkles, Hand, Github, BookOpen } from 'lucide-react';

export default function Home() {
  const [prediction, setPrediction] = useState<string>('Waiting for gesture...');

  return (
    <main className="min-h-screen bg-slate-950 text-white selection:bg-purple-500/30">
      {/* Background Gradients */}
      <div className="fixed inset-0 z-0 overflow-hidden pointer-events-none">
        <div className="absolute top-[-10%] left-[-10%] w-[40%] h-[40%] bg-purple-500/20 blur-[120px] rounded-full" />
        <div className="absolute bottom-[-10%] right-[-10%] w-[40%] h-[40%] bg-blue-500/20 blur-[120px] rounded-full" />
      </div>

      <div className="relative z-10 container mx-auto px-4 py-8 flex flex-col items-center min-h-screen">

        {/* Header */}
        <header className="w-full flex justify-between items-center mb-12">
          <div className="flex items-center gap-2">
            <div className="bg-gradient-to-br from-purple-500 to-blue-600 p-2 rounded-xl">
              <Hand className="w-6 h-6 text-white" />
            </div>
            <h1 className="text-xl font-bold tracking-tight">Hand Sign Recognation</h1>
          </div>

          <nav className="flex gap-4">
            {/* <a href="#" className="text-sm font-medium text-slate-400 hover:text-white transition-colors flex items-center gap-1">
              <BookOpen className="w-4 h-4" /> Dictionary
            </a> */}
            {/* <a href="#" className="text-sm font-medium text-slate-400 hover:text-white transition-colors flex items-center gap-1">
              <Github className="w-4 h-4" /> Source
            </a> */}
          </nav>
        </header>

        {/* content */}
        <div className="grid lg:grid-cols-2 gap-12 w-full max-w-5xl items-start">

          {/* Left Column: Camera */}
          <div className="flex flex-col gap-4">
            <div className="relative group">
              <div className="absolute -inset-1 bg-gradient-to-r from-purple-600 to-blue-600 rounded-2xl blur opacity-25 group-hover:opacity-75 transition duration-1000 group-hover:duration-200"></div>
              <CameraFrame onPrediction={setPrediction} />
            </div>
            <div className="p-4 rounded-xl bg-white/5 border border-white/10 backdrop-blur-sm">
              <h3 className="text-sm font-medium text-slate-400 mb-2 flex items-center gap-2">
                <Sparkles className="w-4 h-4 text-yellow-400" />
                AI Status
              </h3>
              <div className="flex items-center gap-2">
                <span className="w-2 h-2 rounded-full bg-green-500 animate-pulse" />
                <p className="text-sm text-slate-200">Tracking Hands & Ready</p>
              </div>
            </div>
          </div>

          {/* Right Column: Output & Instructions */}
          <div className="flex flex-col gap-6 pt-4">

            <div className="space-y-2">
              <h2 className="text-4xl font-extrabold tracking-tight bg-clip-text text-transparent bg-gradient-to-br from-white to-slate-400">
                Convert gestures<br /> into text instantly.
              </h2>
              <p className="text-slate-400 text-lg leading-relaxed">
                Our AI analyzes your hand movements in real-time to translate sign language into text.
              </p>
            </div>

            {/* Translation Box */}
            <div className="p-8 rounded-3xl bg-slate-900/50 border border-white/10 shadow-2xl backdrop-blur-md relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-purple-500 to-transparent opacity-50" />

              <h3 className="text-sm font-semibold text-slate-500 uppercase tracking-wider mb-4">Translation</h3>
              <div className="flex items-center justify-center min-h-[120px]">
                <span className="text-6xl font-bold text-white tracking-widest drop-shadow-2xl">
                  {prediction}
                </span>
              </div>
            </div>

            {/* Quick Guide */}
            <div className="grid grid-cols-2 gap-4">
              <div className="p-4 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                <div className="w-8 h-8 rounded-full bg-purple-500/20 flex items-center justify-center mb-3">
                  <span className="font-bold text-purple-400">1</span>
                </div>
                <p className="text-sm text-slate-300">Position your hand clearly in the frame.</p>
              </div>
              <div className="p-4 rounded-2xl bg-white/5 border border-white/5 hover:bg-white/10 transition-colors">
                <div className="w-8 h-8 rounded-full bg-blue-500/20 flex items-center justify-center mb-3">
                  <span className="font-bold text-blue-400">2</span>
                </div>
                <p className="text-sm text-slate-300">Wait for the AI to detect the gesture.</p>
              </div>
            </div>

          </div>

        </div>

      </div>
    </main>
  );
}
