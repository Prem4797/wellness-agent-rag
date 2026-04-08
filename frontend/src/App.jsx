import { useState, useRef, useEffect } from 'react';
import { motion, AnimatePresence, useScroll, useTransform } from 'framer-motion';
import { Send, HeartPulse, ChevronDown, Shield, Sparkles, Heart, X, UserCircle } from 'lucide-react';
import axios from 'axios';
import { v4 as uuidv4 } from 'uuid';

/* ─────────────────────────────────────────────
   DATA (Only core features, no hardcoded specialists)
───────────────────────────────────────────── */
const FEATURES = [
  { icon: Heart, title: 'Deeply Empathetic', desc: 'Express yourself naturally. We listen to how you\'re truly feeling, not just the words you type.' },
  { icon: Shield, title: '100% Private', desc: 'Your conversations are strictly confidential. A safe space built just for you.' },
  { icon: Sparkles, title: 'Perfectly Matched', desc: 'Specialists carefully chosen for your specific needs and goals.' },
];

/* ─────────────────────────────────────────────
   HERO SECTION
───────────────────────────────────────────── */
function Hero({ onStart }) {
  const ref = useRef(null);
  const { scrollYProgress } = useScroll({ target: ref, offset: ['start start', 'end start'] });
  const y = useTransform(scrollYProgress, [0, 1], ['0%', '30%']);
  const opacity = useTransform(scrollYProgress, [0, 0.7], [1, 0]);

  return (
    <section ref={ref} className="relative h-screen flex items-center justify-center overflow-hidden">
      {/* Parallax BG image */}
      <motion.div style={{ y }} className="absolute inset-0 z-0">
        <img
          src="https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=1800&q=90"
          alt="Serene landscape"
          className="w-full h-full object-cover object-center scale-110"
        />
        <div className="absolute inset-0 bg-gradient-to-b from-black/50 via-black/30 to-[#f5f5f7]" />
      </motion.div>

      {/* Content */}
      <motion.div style={{ opacity }} className="relative z-10 text-center px-6 max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.2, duration: 0.8 }}
          className="inline-flex items-center gap-2 bg-white/10 backdrop-blur-md border border-white/20 px-4 py-1.5 rounded-full text-white/90 text-sm font-medium mb-8"
        >
          <HeartPulse className="w-3.5 h-3.5 text-[#30d158]" />
          Wellness Matchmaker
        </motion.div>

        <motion.h1
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.35, duration: 0.9 }}
          className="text-white font-semibold tracking-tight leading-none mb-6"
          style={{ fontSize: 'clamp(42px, 7vw, 96px)', letterSpacing: '-0.03em' }}
        >
          Consciousness <br /> Is<br />All there Is
        </motion.h1>

        <motion.p
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.5, duration: 0.8 }}
          className="text-white/70 text-xl sm:text-2xl font-light mb-12 max-w-2xl mx-auto"
          style={{ letterSpacing: '-0.01em' }}
        >
          Tell us how you're feeling. We'll connect you with the perfect wellness expert.
        </motion.p>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.65, duration: 0.8 }}
          className="flex justify-center items-center"
        >
          <button
            onClick={onStart}
            className="bg-white text-gray-900 text-[17px] font-semibold px-10 py-4 rounded-full hover:bg-white/90 transition-all active:scale-95 shadow-2xl shadow-black/30"
          >
            Start a Session
          </button>
        </motion.div>
      </motion.div>

      {/* Scroll cue */}
      <motion.div
        animate={{ y: [0, 8, 0] }}
        transition={{ repeat: Infinity, duration: 2 }}
        className="absolute bottom-10 left-1/2 -translate-x-1/2 z-10 text-white/60"
      >
        <ChevronDown className="w-6 h-6" />
      </motion.div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   FEATURE STRIP
───────────────────────────────────────────── */
function FeatureStrip() {
  return (
    <section className="bg-[#f5f5f7] py-24 px-6">
      <div className="max-w-5xl mx-auto grid grid-cols-1 sm:grid-cols-3 gap-12 text-center">
        {FEATURES.map((f, i) => (
          <motion.div
            key={i}
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            viewport={{ once: true, margin: '-60px' }}
            transition={{ delay: i * 0.12, duration: 0.6 }}
          >
            <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-br from-[#007aff] to-[#5856d6] shadow-lg shadow-blue-500/30 mb-5">
              <f.icon className="w-5 h-5 text-white" />
            </div>
            <h3 className="text-[19px] font-semibold text-gray-900 mb-2" style={{ letterSpacing: '-0.02em' }}>
              {f.title}
            </h3>
            <p className="text-[15px] text-gray-500 leading-relaxed">{f.desc}</p>
          </motion.div>
        ))}
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   STORY SECTION
───────────────────────────────────────────── */
function StorySection() {
  return (
    <section className="bg-white py-0 overflow-hidden">
      <div className="grid grid-cols-1 lg:grid-cols-2 min-h-[600px]">
        {/* Image */}
        <motion.div
          initial={{ opacity: 0, x: -40 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.9 }}
          className="relative overflow-hidden"
          style={{ minHeight: 400 }}
        >
          <img
            src="https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=900&q=85"
            alt="Meditation"
            className="w-full h-full object-cover"
          />
          <div className="absolute inset-0 bg-gradient-to-r from-transparent to-white/10" />
        </motion.div>

        {/* Text */}
        <motion.div
          initial={{ opacity: 0, x: 40 }}
          whileInView={{ opacity: 1, x: 0 }}
          viewport={{ once: true }}
          transition={{ duration: 0.9 }}
          className="flex flex-col justify-center px-12 py-20 bg-white"
        >
          <span className="text-[13px] font-semibold text-[#007aff] uppercase tracking-[0.1em] mb-4">
            How it works
          </span>
          <h2
            className="text-[40px] font-semibold text-gray-900 mb-6 leading-tight"
            style={{ letterSpacing: '-0.03em' }}
          >
            Tell us how<br />you truly feel.
          </h2>
          <p className="text-[17px] text-gray-500 leading-relaxed mb-8 max-w-md">
            No forms, no questionnaires. Just a conversation. Our AI listens deeply, picks up on nuance, and finds the specialist who's genuinely right for you — not just someone who's available.
          </p>
          <div className="space-y-4">
            {['Share what\'s on your mind', 'Get matched in seconds', 'Begin your journey'].map((step, i) => (
              <div key={i} className="flex items-center gap-4">
                <div className="w-7 h-7 rounded-full bg-[#007aff]/10 flex items-center justify-center flex-shrink-0">
                  <span className="text-[12px] font-bold text-[#007aff]">{i + 1}</span>
                </div>
                <span className="text-[15px] text-gray-700 font-medium">{step}</span>
              </div>
            ))}
          </div>
        </motion.div>
      </div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   FULL-BLEED CTA SECTION
───────────────────────────────────────────── */
function CtaSection({ onStart }) {
  return (
    <section className="relative py-36 px-6 overflow-hidden">
      <div className="absolute inset-0">
        <img
          src="https://images.unsplash.com/photo-1499209974431-9dddcece7f88?w=1800&q=85"
          alt="Peaceful nature"
          className="w-full h-full object-cover"
        />
        <div className="absolute inset-0 bg-black/55" />
      </div>

      <motion.div
        initial={{ opacity: 0, y: 30 }}
        whileInView={{ opacity: 1, y: 0 }}
        viewport={{ once: true }}
        className="relative z-10 text-center max-w-2xl mx-auto"
      >
        <h2
          className="text-white font-semibold mb-6"
          style={{ fontSize: 'clamp(32px, 5vw, 56px)', letterSpacing: '-0.03em', lineHeight: 1.1 }}
        >
          Your wellness journey starts with one conversation.
        </h2>
        <p className="text-white/70 text-[18px] mb-10 font-light">
          No pressure, no judgment. Just honest support from people who care.
        </p>
        <button
          onClick={onStart}
          className="bg-white text-gray-900 text-[17px] font-semibold px-8 py-3.5 rounded-full hover:bg-white/90 transition-all active:scale-95 shadow-2xl shadow-black/30"
        >
          Begin for free
        </button>
      </motion.div>
    </section>
  );
}

/* ─────────────────────────────────────────────
   CHAT VIEW
───────────────────────────────────────────── */

// HELPER FUNCTION: Safely parses stringified JSON from the backend
const safeParsePayload = (text) => {
  if (typeof text === 'object' && text !== null) return text;
  if (typeof text === 'string') {
    try {
      const parsed = JSON.parse(text);
      if (parsed.intro || parsed.advisors) return parsed;
    } catch (e) {
      return null; // Not valid JSON, just a normal string
    }
  }
  return null;
};

function ChatView({ onClose }) {
  const [messages, setMessages] = useState([
    {
      id: 'welcome',
      sender: 'ai',
      text: "Hello. I'm your Wellness AI. Describe what you're feeling, and I'll find the right expert for you.",
    },
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [threadId] = useState(() => uuidv4());
  const messagesEndRef = useRef(null);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isLoading]);

  const handleSend = async (e) => {
    e.preventDefault();
    if (!inputValue.trim()) return;

    const userText = inputValue.trim();
    setInputValue('');
    setMessages((prev) => [...prev, { id: uuidv4(), sender: 'user', text: userText }]);
    setIsLoading(true);

    try {
      const response = await axios.post('http://127.0.0.1:8000/chat', {
        user_input: userText,
        thread_id: threadId,
      });
      // response.data.response is now EITHER a string OR a JSON object
      setMessages((prev) => [...prev, { id: uuidv4(), sender: 'ai', text: response.data.response }]);
    } catch {
      setMessages((prev) => [
        ...prev,
        { id: uuidv4(), sender: 'ai', text: "I'm having trouble connecting right now. Please try again in a moment." },
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 z-50 flex flex-col bg-[#f5f5f7]"
    >
      {/* Chat header */}
      <header className="bg-white/70 backdrop-blur-2xl border-b border-black/[0.06] h-14 flex items-center px-6 justify-between flex-shrink-0">
        <div className="flex items-center gap-2.5">
          <div className="bg-gradient-to-br from-[#007aff] to-[#5856d6] p-1.5 rounded-lg shadow">
            <HeartPulse className="w-4 h-4 text-white" />
          </div>
          <span className="text-[17px] font-semibold text-gray-900" style={{ letterSpacing: '-0.02em' }}>
            Wellness AI
          </span>
        </div>
        <button
          onClick={onClose}
          className="w-8 h-8 rounded-full bg-black/5 hover:bg-black/10 flex items-center justify-center transition-colors"
        >
          <X className="w-4 h-4 text-gray-600" />
        </button>
      </header>

      {/* Messages */}
      <main className="flex-1 overflow-y-auto px-4 sm:px-6 py-6 scrollbar-hide">
        <div className="max-w-2xl mx-auto space-y-4">
          <AnimatePresence initial={false}>
            {messages.map((msg) => {
              
              // Determine if it's a rich payload
              const payload = msg.sender === 'ai' ? safeParsePayload(msg.text) : null;

              // 1. Render User Message OR Simple AI Follow-up (String)
              if (msg.sender === 'user' || !payload) {
                // Ensure we display string properly even if the backend accidentally returned a weird object
                const displayText = typeof msg.text === 'string' ? msg.text : JSON.stringify(msg.text);
                
                return (
                  <motion.div
                    key={msg.id}
                    initial={{ opacity: 0, y: 8, scale: 0.97 }}
                    animate={{ opacity: 1, y: 0, scale: 1 }}
                    className={`flex ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    <div
                      className={`max-w-[78%] px-5 py-3.5 text-[15px] leading-relaxed ${
                        msg.sender === 'user'
                          ? 'bg-[#007aff] text-white rounded-[22px] rounded-br-[6px]'
                          : 'bg-white border border-black/[0.06] text-gray-900 rounded-[22px] rounded-bl-[6px] shadow-sm'
                      }`}
                    >
                      <div className="whitespace-pre-wrap">{displayText}</div>
                    </div>
                  </motion.div>
                );
              }

              // 2. Render Rich JSON Response (Object)
              const { intro, advisors, outro } = payload;

              return (
                <motion.div
                  key={msg.id}
                  initial={{ opacity: 0, y: 8, scale: 0.97 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  className="flex flex-col gap-3 justify-start w-full"
                >
                  {/* Intro Text Bubble */}
                  {intro && (
                    <div className="max-w-[85%] sm:max-w-[78%] px-5 py-3.5 text-[15px] leading-relaxed bg-white border border-black/[0.06] text-gray-900 rounded-[22px] rounded-bl-[6px] shadow-sm">
                      <div className="whitespace-pre-wrap">{intro}</div>
                    </div>
                  )}

                  {/* Horizontal Scrollable Advisor Chips */}
                  {advisors && advisors.length > 0 && (
                    <div className="flex overflow-x-auto gap-3 py-2 pb-4 -mx-4 px-4 sm:-mx-0 sm:px-0 scrollbar-hide w-full max-w-[100vw] sm:max-w-2xl">
                      {advisors.map((adv, idx) => (
                        <div 
                          key={idx} 
                          className="min-w-[260px] max-w-[280px] bg-white border border-gray-100 rounded-2xl p-5 shadow-[0_2px_12px_rgba(0,0,0,0.04)] flex flex-col gap-3 shrink-0"
                        >
                          <div className="flex items-center gap-3">
                            <div className="w-10 h-10 rounded-full bg-blue-50 flex items-center justify-center text-[#007aff]">
                              <UserCircle size={24} strokeWidth={1.5} />
                            </div>
                            <div className="font-semibold text-gray-900 text-[15px] leading-tight">
                              {adv.name}
                            </div>
                          </div>
                          
                          {/* Text expands naturally with no line clamping */}
                          <div className="text-[13px] text-gray-500 leading-relaxed">
                            {adv.description}
                          </div>
                          
                          <button 
                            onClick={() => alert(`Maps to profile for ${adv.name}`)}
                            className="mt-auto w-full text-[#007aff] text-[13px] font-semibold bg-blue-50/50 hover:bg-blue-50 transition-colors py-2 rounded-xl"
                          >
                            View Profile
                          </button>
                        </div>
                      ))}
                    </div>
                  )}

                  {/* Outro Text Bubble */}
                  {outro && (
                    <div className="max-w-[85%] sm:max-w-[78%] px-5 py-3.5 text-[15px] leading-relaxed bg-white border border-black/[0.06] text-gray-900 rounded-[22px] rounded-bl-[6px] shadow-sm">
                      <div className="whitespace-pre-wrap">{outro}</div>
                    </div>
                  )}
                </motion.div>
              );
            })}
          </AnimatePresence>

          {isLoading && (
            <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex justify-start">
              <div className="bg-white border border-black/[0.06] px-5 py-4 rounded-[22px] rounded-bl-[6px] shadow-sm flex gap-1.5 items-center">
                {[0, 150, 300].map((delay) => (
                  <div
                    key={delay}
                    className="w-1.5 h-1.5 rounded-full bg-gray-400 animate-bounce"
                    style={{ animationDelay: `${delay}ms` }}
                  />
                ))}
              </div>
            </motion.div>
          )}
          <div ref={messagesEndRef} />
        </div>
      </main>

      {/* Input */}
      <footer className="bg-white/70 backdrop-blur-2xl border-t border-black/[0.06] pt-3 pb-8 px-4 flex-shrink-0">
        <div className="max-w-2xl mx-auto">
          <form onSubmit={handleSend} className="flex items-end gap-3">
            <div className="flex-1 bg-white border border-gray-200 rounded-[24px] shadow-sm flex items-end pr-2 focus-within:border-[#007aff]/40 focus-within:ring-4 focus-within:ring-[#007aff]/10 transition-all">
              <textarea
                value={inputValue}
                onChange={(e) => setInputValue(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter' && !e.shiftKey) {
                    e.preventDefault();
                    handleSend(e);
                  }
                }}
                placeholder="Describe how you're feeling…"
                rows={1}
                className="w-full max-h-32 min-h-[44px] bg-transparent border-0 focus:ring-0 resize-none py-3 px-5 text-[15px] text-gray-900 placeholder:text-gray-400 outline-none"
              />
              <button
                type="submit"
                disabled={!inputValue.trim() || isLoading}
                className="flex-shrink-0 h-9 w-9 mb-1 rounded-full bg-[#007aff] text-white flex items-center justify-center disabled:opacity-30 disabled:bg-gray-300 transition-all active:scale-95"
              >
                <Send size={14} className="ml-0.5" />
              </button>
            </div>
          </form>
          <p className="text-center text-[11px] text-gray-400 mt-2">
            AI can make mistakes. Always verify medical information with a qualified professional.
          </p>
        </div>
      </footer>
    </motion.div>
  );
}

/* ─────────────────────────────────────────────
   FOOTER
───────────────────────────────────────────── */
function Footer() {
  return (
    <footer className="bg-[#f5f5f7] border-t border-black/[0.08] py-12 px-6">
      <div className="max-w-5xl mx-auto">
        <div className="flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="flex items-center gap-2">
            <div className="bg-gradient-to-br from-[#007aff] to-[#5856d6] p-1.5 rounded-lg">
              <HeartPulse className="w-3.5 h-3.5 text-white" />
            </div>
            <span className="text-[15px] font-semibold text-gray-900" style={{ letterSpacing: '-0.02em' }}>
              Wellness Matchmaker
            </span>
          </div>
          <div className="flex gap-8 text-[13px] text-gray-500">
            <a href="#" className="hover:text-gray-900 transition-colors">Privacy</a>
            <a href="#" className="hover:text-gray-900 transition-colors">Terms</a>
            <a href="#" className="hover:text-gray-900 transition-colors">Contact</a>
          </div>
        </div>
        <div className="mt-8 pt-8 border-t border-black/[0.06]">
          <p className="text-[12px] text-gray-400 leading-relaxed max-w-2xl">
            Copyright © 2026 Wellness Matchmaker. All rights reserved. This platform is not a substitute for professional medical advice, diagnosis, or treatment.
          </p>
        </div>
      </div>
    </footer>
  );
}

/* ─────────────────────────────────────────────
   ROOT APP
───────────────────────────────────────────── */
export default function App() {
  const [showChat, setShowChat] = useState(false);

  return (
    <>
      {/* Sticky nav */}
      <nav className="fixed top-0 left-0 right-0 z-40 bg-[rgba(245,245,247,0.72)] backdrop-blur-2xl border-b border-black/[0.06]">
        <div className="max-w-5xl mx-auto px-6 h-[44px] flex items-center justify-between">
          <div className="flex items-center gap-2 cursor-pointer">
            <div className="bg-gradient-to-br from-[#007aff] to-[#5856d6] p-1 rounded-md shadow-sm">
              <HeartPulse className="w-3.5 h-3.5 text-white" />
            </div>
            <span className="text-[15px] font-semibold text-gray-900 tracking-tight">
              Wellness Matchmaker
            </span>
          </div>
          <div className="hidden sm:flex items-center gap-8 text-[13px] text-gray-600">
            <a href="#" className="hover:text-gray-900 transition-colors">How it works</a>
          </div>
          <button
            onClick={() => setShowChat(true)}
            className="bg-[#007aff] text-white text-[13px] font-semibold px-5 py-1.5 rounded-full hover:bg-blue-600 transition-colors shadow-sm shadow-blue-500/20"
          >
            Start Session
          </button>
        </div>
      </nav>

      {/* Scrollable marketing page */}
      <main>
        <Hero onStart={() => setShowChat(true)} />
        <FeatureStrip />
        <StorySection />
        <CtaSection onStart={() => setShowChat(true)} />
      </main>
      <Footer />

      {/* Chat overlay */}
      <AnimatePresence>
        {showChat && <ChatView onClose={() => setShowChat(false)} />}
      </AnimatePresence>
    </>
  );
}