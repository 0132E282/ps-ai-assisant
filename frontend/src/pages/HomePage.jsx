import React, { useState, useEffect, useCallback, useRef } from 'react';
import axios from 'axios';
import { motion, AnimatePresence } from 'framer-motion';
import { Send, Mic, Bot, User, Cpu } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

export default function HomePage({ agentName }) {
    const [chatHistory, setChatHistory] = useState([]);
    const [chatInput, setChatInput] = useState('');
    const [isListening, setIsListening] = useState(false);
    const [botConfig, setBotConfig] = useState({
        eye_color: '#ffffff',
        body_color: '#4f46e5'
    });
    const chatEndRef = useRef(null);

    const fetchHistory = useCallback(async () => {
        try {
            const res = await axios.get(`${API_BASE}/api/chat`);
            setChatHistory(res.data);
        } catch { /* ignore */ }
    }, []);

    const fetchBotConfig = useCallback(async () => {
        try {
            const res = await axios.get(`${API_BASE}/api/settings`);
            if (res.data) {
                setBotConfig({
                    eye_color: res.data.bot_eye_color || '#ffffff',
                    body_color: res.data.bot_body_color || '#4f46e5'
                });
            }
        } catch { /* ignore */ }
    }, []);

    useEffect(() => {
        const init = async () => {
            await fetchHistory();
            await fetchBotConfig();
        };
        init();
        const interval = setInterval(fetchHistory, 3000);
        return () => clearInterval(interval);
    }, [fetchHistory, fetchBotConfig]);

    useEffect(() => {
        chatEndRef.current?.scrollIntoView({ behavior: 'smooth' });
    }, [chatHistory]);

    const handleSend = async () => {
        if (!chatInput.trim()) return;
        // TODO: Implement send message to backend
        setChatInput('');
    };

    return (
        <div className="p-8 flex flex-col h-screen max-h-screen overflow-hidden">
            {/* Single Card containing Header + Chat */}
            <div className="flex-1 bg-white border border-slate-100 rounded-[2rem] overflow-hidden flex flex-col shadow-sm">
                {/* Header Section */}
                <div className="px-8 py-5 border-b border-slate-100 bg-slate-50/50">
                    <div className="flex items-center justify-between">
                        {/* Left: Bot Info */}
                        <div className="flex items-center gap-4">
                            <motion.div
                                animate={{
                                    scale: isListening ? [1, 1.05, 1] : 1
                                }}
                                transition={{ repeat: Infinity, duration: 2 }}
                                className="w-16 h-16 rounded-2xl flex items-center justify-center shadow-lg relative z-10 transition-colors duration-500"
                                style={{ backgroundColor: botConfig.body_color }}
                            >
                                <Bot size={32} style={{ color: botConfig.eye_color }} className="opacity-90" />
                            </motion.div>
                            <div>
                                <h1 className="text-xl font-black tracking-tight text-slate-900">
                                    {agentName || 'PS-Assistant'}
                                </h1>
                                <p className="text-sm text-slate-400 font-medium flex items-center gap-2">
                                    <span className="w-2 h-2 bg-emerald-500 rounded-full animate-pulse" />
                                    {isListening ? "Đang lắng nghe..." : "Sẵn sàng"}
                                </p>
                            </div>
                        </div>

                        {/* Center: Chat Title */}
                        <div>
                            <h2 className="text-lg font-black text-slate-900 uppercase tracking-tighter">
                                Chat Command History
                            </h2>
                        </div>

                        {/* Right: CPU Usage + Live Badge */}
                        <div className="flex items-center gap-6">
                            {/* CPU Usage */}
                            <div className="flex items-center gap-3">
                                <Cpu size={20} className="text-indigo-500" />
                                <div className="flex flex-col gap-1">
                                    <div className="flex items-center gap-2">
                                        <span className="text-xs font-bold text-slate-600">CPU Usage</span>
                                        <span className="text-xs font-black text-indigo-600">79%</span>
                                    </div>
                                    <div className="w-32 bg-slate-100 h-1.5 rounded-full overflow-hidden">
                                        <div className="bg-indigo-600 h-full rounded-full transition-all duration-300" style={{ width: '79%' }} />
                                    </div>
                                </div>
                            </div>

                            {/* Live Badge */}
                            <div className="text-[10px] bg-emerald-50 text-emerald-600 px-3 py-1.5 rounded-lg font-black uppercase tracking-widest border border-emerald-100">
                                Live
                            </div>
                        </div>
                    </div>
                </div>

                {/* Chat Messages */}
                <div className="flex-1 overflow-y-auto p-8 space-y-4 custom-scrollbar">
                    {chatHistory.length === 0 && (
                        <div className="flex flex-col items-center justify-center h-full text-slate-300 space-y-4 opacity-50">
                            <Bot size={50} />
                            <p className="text-sm font-black uppercase tracking-widest">Chưa có tin nhắn</p>
                        </div>
                    )}

                    <AnimatePresence>
                        {chatHistory.map((msg) => (
                            <motion.div
                                key={msg.id}
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0 }}
                                transition={{ duration: 0.3 }}
                                className={`flex ${msg.type === 'user' ? 'justify-end' : 'justify-start'}`}
                            >
                                <div className={`flex gap-3 max-w-[75%] ${msg.type === 'user' ? 'flex-row-reverse' : 'flex-row'}`}>
                                    {/* Avatar */}
                                    <div className={`w-10 h-10 rounded-2xl flex items-center justify-center flex-shrink-0 ${msg.type === 'user'
                                        ? 'bg-gradient-to-br from-emerald-400 to-teal-500'
                                        : 'bg-gradient-to-br from-indigo-500 to-purple-600'
                                        }`}>
                                        {msg.type === 'user' ? (
                                            <User size={20} className="text-white" />
                                        ) : (
                                            <Bot size={20} className="text-white" />
                                        )}
                                    </div>

                                    {/* Message Bubble */}
                                    <div className="flex flex-col gap-1">
                                        <div className={`px-5 py-3 rounded-2xl ${msg.type === 'user'
                                            ? 'bg-gradient-to-br from-emerald-500 to-teal-600 text-white'
                                            : 'bg-slate-100 text-slate-800'
                                            }`}>
                                            {msg.command_type && msg.type === 'assistant' && (
                                                <span className="text-[9px] font-black px-2 py-0.5 bg-white/20 rounded mb-2 inline-block uppercase tracking-widest">
                                                    {msg.command_type}
                                                </span>
                                            )}
                                            <p className="text-sm font-medium leading-relaxed">{msg.message}</p>
                                        </div>
                                        <span className={`text-[10px] font-medium ${msg.type === 'user' ? 'text-right' : 'text-left'
                                            } text-slate-400 px-2`}>
                                            {new Date(msg.timestamp).toLocaleTimeString('vi-VN', {
                                                hour: '2-digit',
                                                minute: '2-digit'
                                            })}
                                        </span>
                                    </div>
                                </div>
                            </motion.div>
                        ))}
                    </AnimatePresence>
                    <div ref={chatEndRef} />
                </div>

                {/* Chat Input */}
                <div className="px-8 py-6 bg-slate-50/50 border-t border-slate-100">
                    <div className="flex gap-4 max-w-full mx-auto items-center">
                        <button
                            onClick={() => setIsListening(!isListening)}
                            className={`w-14 h-14 rounded-2xl flex items-center justify-center transition-all duration-300 shadow-lg ${isListening
                                ? 'bg-rose-500 shadow-rose-200 scale-95'
                                : 'bg-indigo-600 hover:bg-slate-900 shadow-indigo-100'
                                }`}
                        >
                            {isListening ? (
                                <div className="flex gap-1">
                                    {[...Array(3)].map((_, i) => (
                                        <motion.div
                                            key={i}
                                            animate={{ height: [8, 16, 8] }}
                                            transition={{ repeat: Infinity, duration: 0.5, delay: i * 0.1 }}
                                            className="w-1 bg-white rounded-full"
                                        />
                                    ))}
                                </div>
                            ) : (
                                <Mic size={24} className="text-white" />
                            )}
                        </button>
                        <div className="flex-1 relative">
                            <input
                                className="w-full h-14 bg-white border border-slate-200 rounded-2xl px-6 text-base outline-none focus:border-indigo-500 transition-all font-medium text-slate-800 placeholder:text-slate-300 shadow-xs"
                                placeholder="Nhập tin nhắn..."
                                value={chatInput}
                                onChange={e => setChatInput(e.target.value)}
                                onKeyDown={e => e.key === 'Enter' && handleSend()}
                            />
                            <button
                                onClick={handleSend}
                                className="absolute right-4 top-4 text-slate-300 hover:text-indigo-600 transition-colors"
                            >
                                <Send size={20} />
                            </button>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
