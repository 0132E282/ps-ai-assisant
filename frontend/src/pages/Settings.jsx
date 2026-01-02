import React, { useState, useEffect, useCallback, useMemo } from 'react';
import axios from 'axios';
import { Settings as SettingsIcon, Save, Cpu, Bot, Sparkles, Brain, CheckCircle, Palette } from 'lucide-react';

const API_BASE = 'http://127.0.0.1:8000';

export default function SettingsPage({ onSettingsUpdate }) {
    const [promptData, setPromptData] = useState({
        name: 'PS-Assistant',
        personality: 'Thân thiện, hóm hỉnh và lễ phép.',
        role: '',
        ai_provider: 'gemini',
        gemini_model: 'gemini-2.0-flash-exp',
        bot_eye_color: '#ffffff',
        bot_body_color: '#4f46e5'
    });
    const [behaviors, setBehaviors] = useState([]);
    const [availableModels, setAvailableModels] = useState({});

    const fetchSettings = useCallback(async () => {
        try {
            const res = await axios.get(`${API_BASE}/api/settings`);
            if (res.data) {
                setPromptData(prev => ({
                    ...prev,
                    name: res.data.agent_name || prev.name,
                    gemini_model: res.data.gemini_model || prev.gemini_model,
                    bot_eye_color: res.data.bot_eye_color || prev.bot_eye_color,
                    bot_body_color: res.data.bot_body_color || prev.bot_body_color
                }));
            }
        } catch { /* ignore */ }
    }, []);

    const fetchBehaviors = useCallback(async () => {
        try {
            const res = await axios.get(`${API_BASE}/api/behaviors`);
            setBehaviors(res.data);
        } catch { /* ignore */ }
    }, []);

    const fetchModels = useCallback(async () => {
        try {
            const res = await axios.get(`${API_BASE}/api/models`);
            if (res.data && res.data.models) {
                setAvailableModels(res.data.models);
            }
        } catch { /* ignore */ }
    }, []);

    useEffect(() => {
        const init = async () => {
            await fetchSettings();
            await fetchBehaviors();
            await fetchModels();
        };
        init();
    }, [fetchSettings, fetchBehaviors, fetchModels]);

    const systemPrompt = useMemo(() => {
        return `Bạn là ${promptData.name}. 
Tính cách của bạn: ${promptData.personality}
${promptData.role ? 'Vai trò của bạn: ' + promptData.role : ''}

Nhiệm vụ chính: Nhận diện ý định và chuyển thành lệnh JSON.
Trả về JSON: {"type": "...", "params": {...}, "message": "..."}`;
    }, [promptData]);

    const handleSaveBrain = async () => {
        try {
            await axios.post(`${API_BASE}/api/update-prompt`, { prompt: systemPrompt });
            await axios.post(`${API_BASE}/api/settings`, {
                agent_name: promptData.name,
                gemini_model: promptData.gemini_model,
                bot_eye_color: promptData.bot_eye_color,
                bot_body_color: promptData.bot_body_color
            });
            alert("Cấu hình AI đã được lưu!");
            onSettingsUpdate();
        } catch {
            alert("Lỗi khi lưu cấu hình!");
        }
    };

    const executeBehavior = async (id) => {
        await axios.post(`${API_BASE}/api/execute-behavior/${id}`);
        alert("Đã thực thi hành vi!");
    };

    return (
        <div className="bg-white min-h-full">
            <div className="max-w-6xl mx-auto p-12 space-y-12">
                <header className="flex items-end justify-between border-b border-slate-50 pb-10">
                    <div>
                        <h1 className="text-4xl font-black text-slate-900 tracking-tighter mb-2">Cấu hình Hệ thống</h1>
                        <p className="text-slate-400 text-lg font-medium">Thiết lập ý thức và giao diện nhân vật</p>
                    </div>
                    <div className="flex gap-3 mb-2">
                        <div className="flex items-center gap-2 bg-emerald-50 text-emerald-600 px-3 py-1.5 rounded-xl font-black text-[10px] uppercase tracking-widest border border-emerald-100">
                            <CheckCircle size={12} />
                            Connected
                        </div>
                    </div>
                </header>

                <div className="grid grid-cols-1 lg:grid-cols-12 gap-12">
                    {/* Main Form */}
                    <div className="lg:col-span-12 xl:col-span-7 space-y-12">
                        {/* Section: Brain */}
                        <div className="bg-white">
                            <div className="flex items-center gap-4 mb-10">
                                <div className="w-12 h-12 bg-slate-900 rounded-2xl flex items-center justify-center">
                                    <Brain className="text-indigo-400" size={24} />
                                </div>
                                <h2 className="text-xl font-black text-slate-900">Thông số AI</h2>
                            </div>

                            <div className="space-y-10">
                                <div>
                                    <label className="block text-[11px] text-slate-400 uppercase font-black tracking-widest mb-4 ml-1">Tên định danh (Agent Name)</label>
                                    <div className="relative">
                                        <input
                                            className="w-full bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 focus:border-indigo-500 focus:bg-white outline-none transition-all font-bold text-base shadow-xs"
                                            value={promptData.name}
                                            onChange={e => setPromptData({ ...promptData, name: e.target.value })}
                                        />
                                        <Sparkles className="absolute right-4 top-1/2 -translate-y-1/2 text-slate-200" size={18} />
                                    </div>
                                </div>

                                <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
                                    <div>
                                        <label className="block text-[11px] text-slate-400 uppercase font-black tracking-widest mb-4 ml-1">AI Provider</label>
                                        <select
                                            className="w-full bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 font-bold outline-none focus:border-indigo-500 focus:bg-white transition-all appearance-none cursor-pointer text-sm shadow-xs"
                                            value={promptData.ai_provider}
                                            onChange={e => setPromptData({ ...promptData, ai_provider: e.target.value })}
                                        >
                                            <option value="gemini">🤖 Google Gemini</option>
                                            <option value="openai">💬 ChatGPT (OpenAI)</option>
                                            <option value="claude">🧠 Claude (Anthropic)</option>
                                            <option value="llama">🦙 LLaMA (Local/Groq)</option>
                                        </select>
                                    </div>

                                    <div>
                                        <label className="block text-[11px] text-slate-400 uppercase font-black tracking-widest mb-4 ml-1">Tính cách phản hồi</label>
                                        <select
                                            className="w-full bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 font-bold outline-none focus:border-indigo-500 focus:bg-white transition-all appearance-none cursor-pointer text-sm shadow-xs"
                                            value={promptData.personality}
                                            onChange={e => setPromptData({ ...promptData, personality: e.target.value })}
                                        >
                                            <option value="Thân thiện, hóm hỉnh và lễ phép.">Thân thiện, hóm hỉnh & Lễ phép</option>
                                            <option value="Chuyên nghiệp, ngắn gọn và logic.">Chuyên nghiệp, ngắn gọn & Logic</option>
                                            <option value="Robot lạnh lùng, chỉ tập trung vào lệnh.">Robot & Nghiêm túc</option>
                                        </select>
                                    </div>

                                    <div>
                                        <label className="block text-[11px] text-slate-400 uppercase font-black tracking-widest mb-4 ml-1">
                                            {promptData.ai_provider === 'gemini' ? 'Gemini Model' :
                                                promptData.ai_provider === 'openai' ? 'GPT Model' :
                                                    promptData.ai_provider === 'llama' ? 'LLaMA Model' : 'AI Model'}
                                        </label>
                                        <select
                                            className="w-full bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 font-bold outline-none focus:border-indigo-500 focus:bg-white transition-all appearance-none cursor-pointer text-sm shadow-xs"
                                            value={promptData.gemini_model}
                                            onChange={e => setPromptData({ ...promptData, gemini_model: e.target.value })}
                                            disabled={promptData.ai_provider !== 'gemini'}
                                        >
                                            {Object.keys(availableModels).length > 0 ? (
                                                Object.entries(availableModels).map(([name, value]) => (
                                                    <option key={value} value={value}>
                                                        {name}
                                                    </option>
                                                ))
                                            ) : (
                                                <>
                                                    <option value="models/gemini-2.5-flash">Gemini 2.5 Flash (Loading...)</option>
                                                </>
                                            )}
                                        </select>
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-[11px] text-slate-400 uppercase font-black tracking-widest mb-4 ml-1">Chỉ dẫn vai trò chi tiết</label>
                                    <textarea
                                        className="w-full bg-slate-50 border border-slate-100 rounded-2xl p-6 text-slate-900 focus:border-indigo-500 focus:bg-white outline-none transition-all h-40 font-bold text-sm leading-relaxed resize-none shadow-xs"
                                        placeholder="Mô tả nhiệm vụ..."
                                        value={promptData.role}
                                        onChange={e => setPromptData({ ...promptData, role: e.target.value })}
                                    />
                                </div>
                            </div>
                        </div>

                        {/* Section: Appearance */}
                        <div className="pt-10 border-t border-slate-50">
                            <div className="flex items-center gap-4 mb-10">
                                <div className="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center">
                                    <Palette className="text-white" size={24} />
                                </div>
                                <h2 className="text-xl font-black text-slate-900">Ngoại hình Nhân vật</h2>
                            </div>

                            <div className="grid grid-cols-1 md:grid-cols-2 gap-10">
                                <div>
                                    <label className="block text-[11px] text-slate-400 uppercase font-black tracking-widest mb-4 ml-1">Màu sắc Robot (Body)</label>
                                    <div className="flex items-center gap-4">
                                        <input
                                            type="color"
                                            className="w-14 h-14 rounded-2xl overflow-hidden cursor-pointer border-none p-0 bg-transparent shadow-xs"
                                            value={promptData.bot_body_color}
                                            onChange={e => setPromptData({ ...promptData, bot_body_color: e.target.value })}
                                        />
                                        <input
                                            className="flex-1 bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 font-bold outline-none focus:border-indigo-500 shadow-xs uppercase text-sm"
                                            value={promptData.bot_body_color}
                                            onChange={e => setPromptData({ ...promptData, bot_body_color: e.target.value })}
                                        />
                                    </div>
                                </div>

                                <div>
                                    <label className="block text-[11px] text-slate-400 uppercase font-black tracking-widest mb-4 ml-1">Màu hiệu ứng (Eyes/Icon)</label>
                                    <div className="flex items-center gap-4">
                                        <input
                                            type="color"
                                            className="w-14 h-14 rounded-2xl overflow-hidden cursor-pointer border-none p-0 bg-transparent shadow-xs"
                                            value={promptData.bot_eye_color}
                                            onChange={e => setPromptData({ ...promptData, bot_eye_color: e.target.value })}
                                        />
                                        <input
                                            className="flex-1 bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 font-bold outline-none focus:border-indigo-500 shadow-xs uppercase text-sm"
                                            value={promptData.bot_eye_color}
                                            onChange={e => setPromptData({ ...promptData, bot_eye_color: e.target.value })}
                                        />
                                    </div>
                                </div>
                            </div>
                        </div>

                        <button
                            onClick={handleSaveBrain}
                            className="w-full bg-slate-900 hover:bg-indigo-600 py-5 rounded-2xl font-black text-white text-sm flex items-center justify-center gap-3 transition-all active:scale-[0.98] shadow-2xl shadow-indigo-100"
                        >
                            <Save size={18} />
                            LƯU CẤU HÌNH HỆ THỐNG
                        </button>
                    </div>

                    <div className="lg:col-span-12 xl:col-span-5 space-y-12">
                        <div className="bg-slate-50 p-8 rounded-[3rem] border border-slate-100">
                            <div className="flex items-center gap-3 mb-8">
                                <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-sm">
                                    <Bot className="text-slate-400" size={20} />
                                </div>
                                <h2 className="text-lg font-black text-slate-900">Preview Nhân vật</h2>
                            </div>

                            <div className="flex flex-col items-center justify-center py-10 bg-white rounded-[2.5rem] border border-slate-100 shadow-inner">
                                <div
                                    className="w-40 h-40 rounded-[2.5rem] flex items-center justify-center shadow-xl transition-all duration-500"
                                    style={{ backgroundColor: promptData.bot_body_color }}
                                >
                                    <Bot size={70} style={{ color: promptData.bot_eye_color }} className="opacity-90 transition-all duration-500" />
                                </div>
                                <p className="mt-6 text-slate-500 font-black text-[10px] uppercase tracking-[0.2em]">{promptData.name}</p>
                            </div>
                        </div>

                        <div className="bg-slate-50 p-8 rounded-[3rem] border border-slate-100">
                            <div className="flex items-center gap-3 mb-8">
                                <div className="w-10 h-10 bg-white rounded-xl flex items-center justify-center shadow-sm">
                                    <Cpu className="text-slate-400" size={20} />
                                </div>
                                <h2 className="text-lg font-black text-slate-900">Phím tắt nhanh</h2>
                            </div>

                            <div className="grid grid-cols-2 gap-4">
                                {behaviors.map(b => (
                                    <button
                                        key={b.id}
                                        onClick={() => executeBehavior(b.id)}
                                        className="bg-white hover:bg-indigo-600 hover:text-white border border-slate-100 p-5 rounded-2xl flex flex-col items-center gap-4 transition-all group shadow-xs"
                                    >
                                        <div className="w-12 h-12 bg-slate-50 rounded-xl flex items-center justify-center text-indigo-600 text-xl group-hover:bg-white/20 group-hover:text-white transition-all">
                                            ⚡️
                                        </div>
                                        <span className="text-[10px] font-black uppercase tracking-tighter">{b.name}</span>
                                    </button>
                                ))}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    );
}
