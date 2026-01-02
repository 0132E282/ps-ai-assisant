import { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import SidebarLayout from './components/SidebarLayout';
import HomePage from './pages/HomePage';
import AdminPage from './pages/Admin';
import SettingsPage from './pages/Settings';
import axios from 'axios';

const API_BASE = 'http://127.0.0.1:8000';

export default function App() {
  const [settings, setSettings] = useState({
    agent_name: 'PS-Assistant'
  });

  const fetchSettings = async () => {
    try {
      const res = await axios.get(`${API_BASE}/api/settings`);
      if (res.data) {
        setSettings(prev => ({
          ...prev,
          agent_name: res.data.agent_name || prev.agent_name
        }));
      }
    } catch { /* ignore */ }
  };

  useEffect(() => {
    const init = async () => {
      await fetchSettings();
    };
    init();
  }, []);

  return (
    <Router>
      <SidebarLayout agentName={settings.agent_name}>
        <Routes>
          <Route path="/" element={<HomePage agentName={settings.agent_name} />} />
          <Route path="/admin" element={<AdminPage />} />
          <Route path="/settings" element={<SettingsPage onSettingsUpdate={fetchSettings} />} />
        </Routes>
      </SidebarLayout>
    </Router>
  );
}
