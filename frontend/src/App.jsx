import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import QueryInput from './components/QueryInput';
import AgentTrace from './components/AgentTrace';
import ReportPanel from './components/ReportPanel';
import SourcesSidebar from './components/SourcesSidebar';
import FollowUpChat from './components/FollowUpChat';
import { researchService } from './services/researchService';
import { Settings, Menu, X, Dot } from 'lucide-react';

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
    <div className="flex items-center gap-1 group">
      <div className="w-5 h-5 bg-gray-900 rounded-sm relative group-hover:scale-110 transition-transform duration-500">
        <div className="absolute inset-1 bg-white rounded-sm"></div>
        <div className="absolute inset-2 bg-gray-900 rounded-[1px]"></div>
      </div>
      <span className="font-pixel text-xl tracking-wider text-gray-900 ml-2">ARIA.</span>
    </div>
  );

  const pageVariants = {
    initial: { opacity: 0, y: 10 },
    animate: { opacity: 1, y: 0, transition: { duration: 0.8, ease: [0.16, 1, 0.3, 1] } },
    exit: { opacity: 0, y: -10, transition: { duration: 0.4 } }
  };

  const renderHome = () => (
    <motion.div 
      key="home"
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className="flex-1 flex flex-col items-center justify-center p-6 w-full relative overflow-hidden"
    >
      {/* Dense, artistic dot mask background */}
      <div className="absolute inset-0 bg-dots opacity-60 pointer-events-none"></div>

      <div className="relative z-10 w-full max-w-4xl mx-auto px-4 md:px-8 py-16 md:py-24">
        <div className="text-center mb-16 md:mb-24">
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2, duration: 1, ease: "easeOut" }}
            className="text-4xl sm:text-5xl md:text-7xl lg:text-[5.5rem] font-pixel text-gray-900 leading-[0.9] tracking-tighter mb-8 md:mb-12"
          >
            SYNTHESIZE.<br/>RESEARCH.<br/>DISCOVER.
          </motion.h1>
          <motion.p 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6, duration: 1 }}
            className="text-gray-500 font-sans text-base md:text-lg max-w-xl mx-auto leading-relaxed font-light px-4"
          >
            Aria brings AI to a new era of cognitive research. Understand, simulate, and synthesize world knowledge instantly.
          </motion.p>
        </div>

        <div className="w-full max-w-2xl mx-auto">
          <QueryInput onSubmit={handleStartResearch} />
          
          <motion.div 
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.8 }}
            className="mt-20 md:mt-28 flex flex-col items-center"
          >
            <div className="flex flex-wrap justify-center gap-3">
              {[
                "NVIDIA's AI strategy",
                "India's semiconductor ecosystem",
                "OpenAI vs Anthropic"
              ].map((q, i) => (
                <button 
                  key={q} 
                  onClick={() => handleStartResearch(q)}
                  className="px-5 py-2.5 bg-white/50 backdrop-blur-sm border border-gray-200 rounded-full text-xs font-pixel uppercase tracking-widest text-gray-500 hover:text-gray-900 hover:border-gray-900 hover:bg-white transition-all duration-500"
                >
                  {q}
                </button>
              ))}
            </div>
          </motion.div>
        </div>
      </div>
    </motion.div>
  );

  const renderResearching = () => (
    <motion.div 
      key="researching"
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className="flex-1 flex flex-col items-center justify-center p-6"
    >
      <AgentTrace currentStep={progressStep} />
    </motion.div>
  );

  const renderWorkspace = () => (
    <motion.div 
      key="workspace"
      variants={pageVariants}
      initial="initial"
      animate="animate"
      exit="exit"
      className="flex-1 flex flex-col lg:flex-row overflow-hidden relative"
    >
      <div className="flex-1 overflow-y-auto p-6 sm:p-12 lg:p-20 border-r border-gray-200 no-scrollbar relative z-10 bg-white shadow-[0_0_40px_rgba(0,0,0,0.02)]">
        <div className="max-w-3xl mx-auto xl:ml-auto xl:mr-0 2xl:mx-auto">
          <div className="mb-16">
            <h1 className="text-3xl md:text-5xl font-sans font-light text-gray-900 leading-tight tracking-tight mb-8">
              {currentSession.question}
            </h1>
            <div className="flex items-center gap-4 text-xs font-pixel tracking-widest uppercase text-gray-400">
              <span>Intelligence Report</span>
              <span className="w-1 h-1 bg-gray-300"></span>
              <span>{new Date(currentSession.createdAt).toLocaleDateString('en-US', { month: 'short', day: '2-digit', year: 'numeric' })}</span>
            </div>
          </div>
          
          <ReportPanel session={currentSession} />
          
          <div className="block lg:hidden mt-20 pt-10 border-t border-gray-200">
            <SourcesSidebar session={currentSession} />
          </div>

          <div className="mt-24 pt-16 border-t border-gray-200">
            <FollowUpChat session={currentSession} setSession={setCurrentSession} />
          </div>
        </div>
      </div>
      
      <div className="hidden lg:block w-96 bg-gray-50/30 overflow-y-auto border-l border-gray-200 relative">
        <div className="absolute inset-0 bg-dots opacity-20 pointer-events-none"></div>
        <div className="relative z-10">
          <SourcesSidebar session={currentSession} />
        </div>
      </div>
    </motion.div>
  );

  return (
    <div className="flex flex-col h-screen w-full font-sans transition-colors duration-500 overflow-hidden relative bg-[rgb(var(--color-bg))] text-[rgb(var(--color-text))]">
      
      {/* Settings Modal - Kept minimal and stark */}
      <AnimatePresence>
        {isSettingsOpen && (
          <motion.div 
            initial={{ opacity: 0 }} animate={{ opacity: 1 }} exit={{ opacity: 0 }}
            className="fixed inset-0 z-50 flex items-center justify-center bg-gray-900/10 backdrop-blur-sm p-4"
          >
            <motion.div 
              initial={{ scale: 0.95, opacity: 0 }} animate={{ scale: 1, opacity: 1 }} exit={{ scale: 0.95, opacity: 0 }}
              className="bg-white w-full max-w-md shadow-2xl p-8 relative border border-gray-200"
            >
              <button onClick={() => setIsSettingsOpen(false)} className="absolute top-6 right-6 text-gray-400 hover:text-gray-900 transition-colors">
                <X className="w-5 h-5" />
              </button>
              <h2 className="text-xl font-pixel tracking-wider text-gray-900 mb-8 uppercase">Preferences</h2>
              
              <div className="space-y-6">
                <div className="flex items-center justify-between">
                  <h4 className="font-sans font-medium text-gray-900">Theme</h4>
                  <div className="flex gap-1 p-1 bg-gray-50 border border-gray-200">
                    {['light', 'dark'].map(t => (
                      <button 
                        key={t}
                        onClick={() => setPrefs(p => ({...p, theme: t}))}
                        className={`px-4 py-2 text-xs font-pixel uppercase tracking-wider transition-all ${prefs.theme === t ? 'bg-gray-900 text-white' : 'text-gray-500 hover:text-gray-900'}`}
                      >
                        {t}
                      </button>
                    ))}
                  </div>
                </div>
              </div>
            </motion.div>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Header */}
      <header className="flex-none bg-transparent relative z-40">
        <div className="max-w-7xl mx-auto flex justify-between items-center px-6 h-20">
          <div className="flex items-center gap-12">
            <div className="cursor-pointer" onClick={() => setAppState('home')}>
              <Logo />
            </div>
            
            <div className="hidden md:flex items-center gap-8 h-6">
              <button onClick={() => setAppState('home')} className="text-gray-500 hover:text-gray-900 text-xs font-pixel uppercase tracking-widest transition-colors">
                New Query
              </button>
              <button onClick={() => setIsMobileMenuOpen(true)} className="text-gray-500 hover:text-gray-900 text-xs font-pixel uppercase tracking-widest transition-colors">
                History
              </button>
            </div>
          </div>
          
          <div className="flex items-center gap-4">
            <button onClick={() => setIsSettingsOpen(true)} className="w-10 h-10 flex items-center justify-center bg-transparent border border-gray-200 text-gray-500 hover:text-gray-900 hover:border-gray-900 transition-all duration-300">
              <Settings className="w-4 h-4" />
            </button>
          </div>
        </div>
      </header>

      {/* Main Content with framer-motion AnimatePresence */}
      <main className="flex-1 flex flex-col overflow-hidden relative">
        <AnimatePresence mode="wait">
          {appState === 'home' && renderHome()}
          {appState === 'researching' && renderResearching()}
          {appState === 'workspace' && renderWorkspace()}
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
