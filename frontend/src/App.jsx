import React, { useState, useEffect } from 'react';
import QueryInput from './components/QueryInput';
import AgentTrace from './components/AgentTrace';
import ReportPanel from './components/ReportPanel';
import SourcesSidebar from './components/SourcesSidebar';
import FollowUpChat from './components/FollowUpChat';
import { researchService } from './services/researchService';
import { Search, History, Settings, Menu, X, Sparkles } from 'lucide-react';

function App() {
  const [appState, setAppState] = useState('home'); 
  const [currentSession, setCurrentSession] = useState(null);
  const [progressStep, setProgressStep] = useState('');
  const [history, setHistory] = useState([]);
  const [isMobileMenuOpen, setIsMobileMenuOpen] = useState(false);
  const [isSettingsOpen, setIsSettingsOpen] = useState(false);
  const [prefs, setPrefs] = useState({ deepResearch: true, personalized: false, exportFormat: 'Markdown', theme: 'light' });

  useEffect(() => {
    researchService.getSessions().then(setHistory);
  }, []);

  useEffect(() => {
    document.documentElement.setAttribute('data-theme', prefs.theme);
  }, [prefs.theme]);

  const handleStartResearch = async (question) => {
    setIsMobileMenuOpen(false);
    setAppState('researching');
    try {
      const session = await researchService.startResearch(question, (step) => {
        setProgressStep(step);
      });
      setCurrentSession(session);
      setAppState('workspace');
      researchService.getSessions().then(setHistory);
    } catch (err) {
      console.error(err);
      setAppState('home');
    }
  };

  const handleSelectHistory = async (id) => {
    setIsMobileMenuOpen(false);
    const session = await researchService.getSession(id);
    if (session) {
      setCurrentSession(session);
      setAppState('workspace');
    }
  };

  const Logo = () => (
    <div className="flex items-center gap-2">
      <Sparkles className="w-5 h-5 text-gray-900" />
      <span className="font-sans font-bold text-lg tracking-wide text-gray-900">Aria</span>
    </div>
  );

  const renderHome = () => (
    <div className="flex-1 flex flex-col items-center justify-center p-6 animate-fade-in w-full bg-white relative overflow-hidden">
      
      {/* Background Dots */}
      <div className="absolute inset-0 bg-dots opacity-40 pointer-events-none"></div>

      {/* Subtle Glows */}
      <div className="absolute top-1/3 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[600px] h-[400px] bg-gray-100 rounded-full blur-[100px] opacity-50 pointer-events-none"></div>

      <div className="relative z-10 w-full max-w-2xl mx-auto px-4 md:px-8 py-16">
        <div className="text-center mb-10">
          <h1 className="text-4xl md:text-[2.75rem] font-sans font-medium text-gray-900 leading-tight tracking-tight mb-4">
            Research with clarity.
          </h1>
          <p className="text-gray-500 font-sans text-lg max-w-md mx-auto leading-relaxed font-light">
            Transform complex data into clear, engaging insights. Everything you need in one place.
          </p>
        </div>

        <div className="w-full max-w-xl mx-auto">
          <QueryInput onSubmit={handleStartResearch} />
          
          <div className="mt-12 flex flex-col items-center">
            <div className="flex flex-wrap justify-center gap-2">
              {[
                "NVIDIA's AI strategy",
                "India's semiconductor ecosystem",
                "OpenAI vs Anthropic"
              ].map((q, i) => (
                <button 
                  key={q} 
                  onClick={() => handleStartResearch(q)}
                  className="px-4 py-2 bg-gray-50 border border-gray-100/60 rounded-full text-[13px] font-medium text-gray-500 hover:text-gray-900 hover:bg-gray-100 hover:border-gray-200 transition-all duration-300"
                >
                  {q}
                </button>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );

  const renderResearching = () => (
    <div className="flex-1 flex flex-col items-center justify-center p-6 animate-fade-in bg-grain">
      <AgentTrace currentStep={progressStep} />
    </div>
  );

  const renderWorkspace = () => (
    <div className="flex-1 flex flex-col lg:flex-row overflow-hidden animate-fade-in bg-white relative">
      <div className="flex-1 overflow-y-auto p-6 sm:p-12 lg:p-20 border-r border-gray-100 no-scrollbar relative z-10">
        <div className="max-w-3xl mx-auto xl:ml-auto xl:mr-0 2xl:mx-auto">
          <div className="mb-12 animate-fade-in">
            <h1 className="text-3xl md:text-4xl lg:text-5xl font-sans font-semibold text-gray-900 leading-tight tracking-tight mb-6">
              {currentSession.question}
            </h1>
            <div className="flex items-center gap-4 text-sm text-gray-400 font-medium">
              <span>Intelligence Report</span>
              <span className="w-1 h-1 rounded-full bg-gray-300"></span>
              <span>{new Date(currentSession.createdAt).toLocaleDateString('en-US', { month: 'long', day: 'numeric', year: 'numeric' })}</span>
            </div>
          </div>
          
          <ReportPanel session={currentSession} />
          
          <div className="block lg:hidden mt-16 pt-8 border-t border-gray-100">
            <SourcesSidebar session={currentSession} />
          </div>

          <div className="mt-20 pt-12 border-t border-gray-100">
            <FollowUpChat session={currentSession} setSession={setCurrentSession} />
          </div>
        </div>
      </div>
      
      <div className="hidden lg:block w-96 bg-gray-50/50 overflow-y-auto border-l border-gray-100">
        <SourcesSidebar session={currentSession} />
      </div>
    </div>
  );

  return (
    <div className="flex flex-col h-screen w-full font-sans transition-colors duration-500 overflow-hidden relative">
      
      {/* Settings Modal */}
      {isSettingsOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/20 backdrop-blur-sm animate-fade-in p-4">
          <div className="bg-white w-full max-w-md rounded-2xl shadow-2xl p-8 relative border border-gray-100">
            <button onClick={() => setIsSettingsOpen(false)} className="absolute top-6 right-6 text-gray-400 hover:text-gray-900 transition-colors">
              <X className="w-5 h-5" />
            </button>
            <h2 className="text-xl font-semibold text-gray-900 mb-8">Preferences</h2>
            
            <div className="space-y-6">
              <div className="flex items-center justify-between">
                <div>
                  <h4 className="font-medium text-gray-900">Theme</h4>
                </div>
                <div className="flex gap-1 p-1 bg-gray-50 rounded-lg border border-gray-100">
                  {['light', 'dark'].map(t => (
                    <button 
                      key={t}
                      onClick={() => setPrefs(p => ({...p, theme: t}))}
                      className={`px-3 py-1.5 rounded-md text-xs font-medium capitalize transition-all ${prefs.theme === t ? 'bg-white shadow-sm text-gray-900 border border-gray-200/50' : 'text-gray-500 hover:text-gray-900'}`}
                    >
                      {t}
                    </button>
                  ))}
                </div>
              </div>

              <div className="flex items-center justify-between pt-6 border-t border-gray-50">
                <div>
                  <h4 className="font-medium text-gray-900">Deep Research</h4>
                  <p className="text-xs text-gray-500 mt-1">Enable multi-agent synthesis</p>
                </div>
                <div 
                  onClick={() => setPrefs(p => ({...p, deepResearch: !p.deepResearch}))}
                  className={`w-12 h-6 rounded-full relative cursor-pointer transition-colors duration-300 ${prefs.deepResearch ? 'bg-gray-900' : 'bg-gray-200'}`}
                >
                  <div className={`w-4 h-4 bg-white rounded-full absolute top-1 shadow-sm transition-all duration-300 ${prefs.deepResearch ? 'left-7' : 'left-1'}`}></div>
                </div>
              </div>
              
              <div className="flex items-center justify-between pt-6 border-t border-gray-50">
                <div>
                  <h4 className="font-medium text-gray-900">Export Format</h4>
                </div>
                <div className="flex gap-1 p-1 bg-gray-50 rounded-lg border border-gray-100">
                  {['Markdown', 'PDF'].map(fmt => (
                    <button 
                      key={fmt}
                      onClick={() => setPrefs(p => ({...p, exportFormat: fmt}))}
                      className={`px-3 py-1.5 rounded-md text-xs font-medium transition-all ${prefs.exportFormat === fmt ? 'bg-white shadow-sm text-gray-900 border border-gray-200/50' : 'text-gray-500 hover:text-gray-900'}`}
                    >
                      {fmt}
                    </button>
                  ))}
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Header */}
      <header className="flex-none bg-white/80 backdrop-blur-md border-b border-gray-100 z-40 relative">
        <div className="max-w-7xl mx-auto flex justify-between items-center px-6 h-16">
          <div className="flex items-center gap-8">
            <div className="cursor-pointer" onClick={() => setAppState('home')}>
              <Logo />
            </div>
            
            <div className="hidden md:flex items-center gap-6 border-l border-gray-100 pl-8 h-6">
              <button onClick={() => setAppState('home')} className="text-gray-500 hover:text-gray-900 text-sm font-medium transition-colors">
                New
              </button>
              <button onClick={() => setIsMobileMenuOpen(true)} className="text-gray-500 hover:text-gray-900 text-sm font-medium transition-colors">
                History
              </button>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <button onClick={() => setIsSettingsOpen(true)} className="w-8 h-8 flex items-center justify-center rounded-full bg-gray-50 text-gray-500 hover:text-gray-900 transition-colors">
              <Settings className="w-4 h-4" />
            </button>
            <button onClick={() => setIsMobileMenuOpen(true)} className="md:hidden text-gray-500 hover:text-gray-900">
              <Menu className="w-5 h-5" />
            </button>
          </div>
        </div>
      </header>

      {/* Mobile Menu Drawer */}
      {isMobileMenuOpen && (
        <div className="md:hidden fixed inset-0 z-50 bg-white flex flex-col animate-fade-in">
          <div className="flex items-center justify-between p-6 border-b border-gray-50">
            <Logo />
            <button onClick={() => setIsMobileMenuOpen(false)} className="text-gray-400 hover:text-gray-900">
              <X className="w-5 h-5" />
            </button>
          </div>
          <div className="p-6 overflow-y-auto">
            <p className="text-sm font-medium text-gray-400 mb-6">Recent History</p>
            <div className="space-y-4">
              {history.map((session) => (
                <button 
                  key={session.id}
                  onClick={() => handleSelectHistory(session.id)}
                  className="w-full text-left text-base font-medium text-gray-700 hover:text-gray-900"
                >
                  {session.question}
                </button>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* Main Content */}
      <main className="flex-1 flex flex-col bg-white overflow-hidden relative">
        {appState === 'home' && renderHome()}
        {appState === 'researching' && renderResearching()}
        {appState === 'workspace' && renderWorkspace()}
      </main>
    </div>
  );
}

export default App;
