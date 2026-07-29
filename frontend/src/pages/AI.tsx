import { useState } from "react";
import { Card } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import { Textarea } from "@/components/ui/textarea";
import { ScrollArea } from "@/components/ui/scroll-area";
import { Avatar, AvatarFallback } from "@/components/ui/avatar";
import { Cpu, Send, Bot, User } from "lucide-react";

interface Message {
  id: string;
  role: "user" | "ai";
  content: string;
}

export function AI() {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: "1",
      role: "ai",
      content: "Hello! I am KAIROS AI. I can help you analyze incidents, query logs, or manage system configurations. How can I assist you today?"
    }
  ]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);

  const handleSend = () => {
    if (!input.trim()) return;
    
    const newUserMsg: Message = { id: Date.now().toString(), role: "user", content: input };
    setMessages(prev => [...prev, newUserMsg]);
    setInput("");
    setIsTyping(true);

    // Mock AI Response
    setTimeout(() => {
      const aiResponse: Message = { 
        id: (Date.now() + 1).toString(), 
        role: "ai", 
        content: "I am currently running in a simulated frontend environment. Once the backend AI agent is fully wired, I will provide real-time diagnostic analysis and action execution."
      };
      setMessages(prev => [...prev, aiResponse]);
      setIsTyping(false);
    }, 1500);
  };

  return (
    <div className="flex flex-col h-[calc(100vh-12rem)] space-y-4">
      <div className="flex items-center gap-2 mb-2">
        <Cpu className="h-8 w-8 text-primary" />
        <div>
          <h1 className="text-3xl font-bold tracking-tight text-foreground">KAIROS AI</h1>
          <p className="text-muted-foreground text-sm">Your autonomous operational assistant.</p>
        </div>
      </div>

      <Card className="flex-1 flex flex-col border-border shadow-md overflow-hidden bg-background">
        <ScrollArea className="flex-1 p-4">
          <div className="space-y-6 max-w-4xl mx-auto py-4">
            {messages.map((msg) => (
              <div key={msg.id} className={`flex gap-4 ${msg.role === "user" ? "flex-row-reverse" : ""}`}>
                <Avatar className="h-10 w-10 border border-border">
                  {msg.role === "ai" ? (
                    <AvatarFallback className="bg-primary/20 text-primary"><Bot size={20} /></AvatarFallback>
                  ) : (
                    <AvatarFallback className="bg-secondary text-foreground"><User size={20} /></AvatarFallback>
                  )}
                </Avatar>
                <div className={`rounded-lg p-4 max-w-[80%] ${
                  msg.role === "ai" 
                    ? "bg-secondary/50 text-foreground" 
                    : "bg-primary text-primary-foreground"
                }`}>
                  <p className="text-sm leading-relaxed whitespace-pre-wrap">{msg.content}</p>
                </div>
              </div>
            ))}
            {isTyping && (
              <div className="flex gap-4">
                <Avatar className="h-10 w-10 border border-border">
                  <AvatarFallback className="bg-primary/20 text-primary"><Bot size={20} /></AvatarFallback>
                </Avatar>
                <div className="rounded-lg p-4 bg-secondary/50 text-foreground flex items-center gap-1">
                  <span className="animate-bounce inline-block">.</span>
                  <span className="animate-bounce inline-block" style={{ animationDelay: '0.2s' }}>.</span>
                  <span className="animate-bounce inline-block" style={{ animationDelay: '0.4s' }}>.</span>
                </div>
              </div>
            )}
          </div>
        </ScrollArea>
        
        <div className="p-4 border-t border-border bg-card">
          <div className="max-w-4xl mx-auto relative flex items-end gap-2">
            <Textarea 
              placeholder="Ask KAIROS to analyze logs, trigger a workflow, or explain an alert..." 
              className="min-h-[60px] resize-none pr-14"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
            />
            <Button 
              size="icon" 
              className="absolute right-2 bottom-2 h-10 w-10" 
              onClick={handleSend}
              disabled={!input.trim() || isTyping}
            >
              <Send className="h-4 w-4" />
            </Button>
          </div>
        </div>
      </Card>
    </div>
  );
}
