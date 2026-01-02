import React, { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import { Plus, Trash2, Play, Save, X, Cpu, Terminal, Layers } from 'lucide-react';
import { motion as Motion } from 'framer-motion';

const API_BASE = 'http://127.0.0.1:8000';

export default function AdminPage() {
    const [behaviors, setBehaviors] = useState([]);
    const [isAdding, setIsAdding] = useState(false);
    const [newBehavior, setNewBehavior] = useState({
        name: '',
        command_type: 'open_app',
        params: '{}',
        icon: 'Zap',
        trigger_keywords: '',
        description: ''
    });

    const fetchBehaviors = useCallback(async () => {
        try {
            const res = await axios.get(`${API_BASE}/api/behaviors`);
            setBehaviors(res.data);
        } catch (err) {
            console.error("Failed to fetch behaviors", err);
        }
    }, []);

    useEffect(() => {
        const load = async () => {
            await fetchBehaviors();
        };
        load();
    }, [fetchBehaviors]);

    const handleAdd = async (e) => {
        e.preventDefault();
        try {
            const payload = {
                ...newBehavior,
                params: typeof newBehavior.params === 'string' ? JSON.parse(newBehavior.params) : newBehavior.params
            };
            await axios.post(`${API_BASE}/api/add-behavior`, payload);
            setIsAdding(false);
            setNewBehavior({
                name: '',
                command_type: 'open_app',
                params: '{}',
                icon: 'Zap',
                trigger_keywords: '',
                description: ''
            });
            fetchBehaviors();
        } catch {
            alert("Lỗi: Kiểm tra định dạng JSON của Params");
        }
    };

    const handleDelete = async (id) => {
        if (window.confirm("Bạn có chắc chắn muốn xóa hành vi này?")) {
            await axios.delete(`${API_BASE}/api/behavior/${id}`);
            fetchBehaviors();
        }
    };

    return (
        <div className="p-12 max-w-7xl mx-auto space-y-10">
            <div className="flex justify-between items-end border-b border-slate-50 pb-8">
                <div>
                    <h1 className="text-4xl font-black text-slate-900 tracking-tighter mb-2">Hành vi Robot</h1>
                    <p className="text-slate-400 font-medium text-lg">Thiết kế logic và lệnh tự động</p>
                </div>
                <button
                    onClick={() => setIsAdding(true)}
                    className="flex items-center gap-2 bg-slate-900 hover:bg-indigo-600 text-white font-black px-8 py-4 rounded-2xl transition-all shadow-xl active:scale-95 text-xs"
                >
                    <Plus size={20} />
                    THÊM HÀNH VI
                </button>
            </div>

            {isAdding && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-6 bg-slate-900/10 backdrop-blur-md">
                    <Motion.div
                        initial={{ opacity: 0, scale: 0.95 }}
                        animate={{ opacity: 1, scale: 1 }}
                        className="bg-white border border-slate-100 p-10 rounded-[3rem] shadow-2xl w-full max-w-2xl relative"
                    >
                        <div className="flex justify-between items-center mb-10">
                            <h2 className="text-2xl font-black text-slate-900 tracking-tight">Thêm hành vi mới</h2>
                            <button onClick={() => setIsAdding(false)} className="w-10 h-10 flex items-center justify-center bg-slate-50 text-slate-400 hover:text-rose-500 rounded-full">
                                <X size={24} />
                            </button>
                        </div>

                        <form onSubmit={handleAdd} className="space-y-8">
                            <div className="grid grid-cols-2 gap-8">
                                <div>
                                    <label className="block text-[11px] text-slate-400 font-black uppercase tracking-widest mb-4 ml-1">Tên hành vi</label>
                                    <input
                                        className="w-full bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 font-bold outline-none focus:border-indigo-500 transition-all font-sans"
                                        value={newBehavior.name}
                                        onChange={e => setNewBehavior({ ...newBehavior, name: e.target.value })}
                                        placeholder="VD: Mở Chrome"
                                        required
                                    />
                                </div>
                                <div>
                                    <label className="block text-[11px] text-slate-400 font-black uppercase tracking-widest mb-4 ml-1">Loại tập lệnh</label>
                                    <select
                                        className="w-full bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 font-bold outline-none focus:border-indigo-500 appearance-none cursor-pointer"
                                        value={newBehavior.command_type}
                                        onChange={e => setNewBehavior({ ...newBehavior, command_type: e.target.value })}
                                    >
                                        <option value="open_app">🖥 Mở ứng dụng</option>
                                        <option value="move">🤖 Di chuyển</option>
                                        <option value="stop">🛑 Dừng</option>
                                        <option value="chat">💬 Phản hồi</option>
                                    </select>
                                </div>
                            </div>

                            <div>
                                <label className="block text-[11px] text-slate-400 font-black uppercase tracking-widest mb-4 ml-1">Tham số (JSON Format)</label>
                                <textarea
                                    className="w-full bg-slate-950 border border-slate-900 rounded-2xl p-6 text-emerald-400 font-mono text-sm h-40 outline-none shadow-inner"
                                    value={newBehavior.params}
                                    onChange={e => setNewBehavior({ ...newBehavior, params: e.target.value })}
                                    placeholder='{"app_name": "Chrome"}'
                                    required
                                />
                            </div>

                            <div className="grid grid-cols-1 gap-8">
                                <div>
                                    <label className="block text-[11px] text-slate-400 font-black uppercase tracking-widest mb-4 ml-1">
                                        🎯 Từ khóa kích hoạt (Trigger Keywords)
                                    </label>
                                    <input
                                        className="w-full bg-gradient-to-br from-violet-50 to-indigo-50 border-2 border-indigo-100 rounded-2xl p-4 text-slate-900 font-bold outline-none focus:border-indigo-500 focus:bg-white transition-all placeholder:text-indigo-300"
                                        value={newBehavior.trigger_keywords}
                                        onChange={e => setNewBehavior({ ...newBehavior, trigger_keywords: e.target.value })}
                                        placeholder="VD: mở chrome, khởi động chrome, chrome đi"
                                    />
                                    <p className="text-xs text-slate-400 mt-2 ml-1 font-medium">
                                        💡 Cách nhau bởi dấu phẩy. Khi nói đúng từ khóa sẽ tự động thực thi!
                                    </p>
                                </div>

                                <div>
                                    <label className="block text-[11px] text-slate-400 font-black uppercase tracking-widest mb-4 ml-1">
                                        📝 Mô tả hành vi
                                    </label>
                                    <textarea
                                        className="w-full bg-slate-50 border border-slate-100 rounded-2xl p-4 text-slate-900 font-medium outline-none focus:border-indigo-500 focus:bg-white transition-all h-24 resize-none"
                                        value={newBehavior.description}
                                        onChange={e => setNewBehavior({ ...newBehavior, description: e.target.value })}
                                        placeholder="Mô tả chi tiết hành vi này làm gì..."
                                    />
                                </div>
                            </div>

                            <button type="submit" className="w-full bg-indigo-600 py-5 rounded-2xl font-black text-white text-base hover:bg-slate-900 transition-all active:scale-95 shadow-2xl shadow-indigo-100">
                                LƯU HÀNH VI
                            </button>
                        </form>
                    </Motion.div>
                </div>
            )}


            <div className="bg-white border border-slate-100 rounded-[2.5rem] overflow-hidden shadow-sm relative">
                <div className="p-8 border-b border-slate-50 bg-slate-50/50 flex items-center justify-between">
                    <div className="flex items-center gap-2">
                        <Terminal size={18} className="text-slate-400" />
                        <span className="text-[11px] font-black text-slate-400 uppercase tracking-widest">Database Content</span>
                    </div>
                </div>

                <div className="overflow-x-auto">
                    <table className="w-full text-left">
                        <thead className="bg-slate-50 text-slate-400 text-[10px] uppercase font-black tracking-[0.2em]">
                            <tr>
                                <th className="px-10 py-6">Hành vi</th>
                                <th className="px-10 py-6">🎯 Trigger</th>
                                <th className="px-10 py-6">Mã thực thi</th>
                                <th className="px-10 py-6">Tham số xử lý</th>
                                <th className="px-10 py-6 text-right">Thao tác</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-slate-50">
                            {behaviors.map(b => (
                                <tr key={b.id} className="hover:bg-slate-50 transition-all group">
                                    <td className="px-10 py-6">
                                        <div className="flex items-center gap-4">
                                            <div className="w-12 h-12 bg-white border border-slate-100 rounded-2xl flex items-center justify-center text-indigo-500 shadow-sm group-hover:bg-slate-900 group-hover:text-white transition-all">
                                                <Layers size={18} />
                                            </div>
                                            <div>
                                                <div className="font-bold text-slate-900 text-base">{b.name}</div>
                                                {b.description && (
                                                    <div className="text-xs text-slate-400 mt-1 font-medium">{b.description}</div>
                                                )}
                                            </div>
                                        </div>
                                    </td>
                                    <td className="px-10 py-6">
                                        {b.trigger_keywords ? (
                                            <div className="flex flex-wrap gap-1.5">
                                                {b.trigger_keywords.split(',').slice(0, 3).map((kw, idx) => (
                                                    <span key={idx} className="px-2 py-1 bg-violet-50 border border-violet-100 text-violet-700 rounded-lg text-[10px] font-black">
                                                        {kw.trim()}
                                                    </span>
                                                ))}
                                                {b.trigger_keywords.split(',').length > 3 && (
                                                    <span className="px-2 py-1 bg-slate-50 text-slate-400 rounded-lg text-[10px] font-black">
                                                        +{b.trigger_keywords.split(',').length - 3}
                                                    </span>
                                                )}
                                            </div>
                                        ) : (
                                            <span className="text-slate-300 text-xs italic">Không có</span>
                                        )}
                                    </td>
                                    <td className="px-10 py-6">
                                        <span className="px-3 py-1.5 bg-white border border-slate-100 text-slate-500 rounded-lg text-[10px] font-black uppercase tracking-widest">
                                            {b.command_type}
                                        </span>
                                    </td>
                                    <td className="px-10 py-6">
                                        <code className="text-xs font-mono font-bold text-indigo-400 opacity-60">
                                            {JSON.stringify(b.params)}
                                        </code>
                                    </td>
                                    <td className="px-10 py-6 text-right">
                                        <button
                                            onClick={() => handleDelete(b.id)}
                                            className="w-10 h-10 flex items-center justify-center rounded-xl text-slate-300 hover:text-rose-500 transition-all"
                                        >
                                            <Trash2 size={20} />
                                        </button>
                                    </td>
                                </tr>
                            ))}
                        </tbody>
                    </table>
                </div>

                {behaviors.length === 0 && (
                    <div className="p-24 text-center text-slate-300 font-bold italic">
                        Chưa có hành vi nào được thiết lập.
                    </div>
                )}
            </div>
        </div>
    );
}
