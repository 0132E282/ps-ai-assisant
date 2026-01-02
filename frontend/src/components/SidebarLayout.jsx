import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { Settings, Cpu, ChevronRight, Bot } from 'lucide-react';

export default function SidebarLayout({ children, agentName }) {
    const location = useLocation();

    const links = [
        { to: '/', label: 'Assistant', icon: Bot },
        { to: '/admin', label: 'Quản lý Hành vi', icon: Cpu },
        { to: '/settings', label: 'Cấu hình Brain', icon: Settings },
    ];

    return (
        <div className="flex min-h-screen bg-[#f8fafc] text-[#0f172a] font-sans selection:bg-indigo-100">
            {/* Sidebar - Fixed */}
            <div className="fixed left-0 top-0 h-screen w-64 border-r border-slate-200 bg-white p-6 flex flex-col overflow-y-auto z-50">
                {/* Header */}
                <div className="flex items-center gap-3 mb-12 px-2">
                    <div className="w-12 h-12 bg-indigo-600 rounded-2xl flex items-center justify-center shadow-lg">
                        <Bot className="text-white" size={24} />
                    </div>
                    <div>
                        <h1 className="text-lg font-black text-slate-900 tracking-tight">
                            {agentName || 'PS-Assistant'}
                        </h1>
                        <div className="flex items-center gap-1.5">
                            <div className="w-1.5 h-1.5 bg-emerald-500 rounded-full animate-pulse" />
                            <span className="text-[10px] font-medium text-slate-400 uppercase tracking-wider">
                                Active System
                            </span>
                        </div>
                    </div>
                </div>

                {/* Navigation */}
                <nav className="flex-1 space-y-2">
                    {links.map((link) => {
                        const Icon = link.icon;
                        const isActive = location.pathname === link.to;
                        return (
                            <Link
                                key={link.to}
                                to={link.to}
                                className={`flex items-center justify-between px-4 py-3 rounded-2xl transition-all duration-200 group ${isActive
                                    ? 'bg-slate-900 text-white shadow-lg'
                                    : 'text-slate-600 hover:bg-slate-50 hover:text-slate-900'
                                    }`}
                            >
                                <div className="flex items-center gap-3">
                                    <Icon
                                        size={20}
                                        className={isActive ? 'text-indigo-400' : 'text-slate-400 group-hover:text-indigo-500'}
                                    />
                                    <span className="font-semibold text-sm">
                                        {link.label}
                                    </span>
                                </div>
                                {isActive && <ChevronRight size={16} className="text-white/40" />}
                            </Link>
                        );
                    })}
                </nav>

                {/* Footer - Core Status */}
                <div className="mt-auto pt-6 border-t border-slate-100">
                    <div className="px-2">
                        <div className="flex items-center justify-between mb-3">
                            <span className="text-[10px] text-slate-400 font-bold uppercase tracking-widest">
                                Core Status
                            </span>
                            <span className="text-[9px] font-black text-indigo-600 bg-indigo-50 px-2 py-0.5 rounded">
                                PRO
                            </span>
                        </div>
                        <div className="flex items-center gap-3">
                            <div className="w-9 h-9 bg-slate-50 rounded-xl flex items-center justify-center border border-slate-100">
                                <Cpu size={18} className="text-slate-500" />
                            </div>
                            <div className="flex-1">
                                <div className="h-1.5 w-full bg-slate-100 rounded-full overflow-hidden">
                                    <div className="h-full bg-indigo-600 rounded-full transition-all duration-300" style={{ width: '79%' }} />
                                </div>
                                <div className="text-[10px] text-slate-500 font-semibold mt-1.5">
                                    CPU Usage 79%
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            </div>

            {/* Main Content */}
            <div className="flex-1 ml-64 overflow-auto bg-[#f8fafc]">
                {children}
            </div>
        </div>
    );
}
