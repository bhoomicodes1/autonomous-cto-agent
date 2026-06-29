import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeRaw from "rehype-raw";

import { Prism as SyntaxHighlighter } from "react-syntax-highlighter";
import { oneDark } from "react-syntax-highlighter/dist/esm/styles/prism";

import api from "./api/api";
import "./App.css";
import FileTree from "./components/FileTree";

import ArchitectureGraph from "./components/ArchitectureGraph";

function App() {
  const [graph, setGraph] = useState(null);
  const [tree, setTree] = useState(null);
  const [githubUrl, setGithubUrl] = useState("");
  const [query, setQuery] = useState("");
  const [owner, setOwner] = useState("");
  const [repo, setRepo] = useState("");
  const [files, setFiles] = useState([]);

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([
  {
    role: "assistant",
    content: `
# 🚀 Autonomous CTO Agent

Analyze any GitHub repository using **RAG + LangGraph + Gemini**.

### Capabilities
🏗 Architecture
📂 Files
🧠 Q&A
⚠ Technical Debt
📊 Health Score

Paste a repository above and click **Analyze Repository**.
`,
  },
]);

  const [analysis, setAnalysis] = useState("");
  const [health, setHealth] = useState(null);
  //const [analyzing, setAnalyzing] = useState(false);

  const sendMessage = async () => {
    if (!query.trim()) return;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        content: query,
      },
    ]);

    setLoading(true);

    try {
      const res = await api.post("/chat/", {
        query,
        owner,
        repo,
      });

      const sources =
  res.data.sources?.map(
    (s) => `• ${s.doc_id}`
  ).join("\n") || "";

setMessages((prev) => [
  ...prev,
  {
    role: "assistant",
    content:
      res.data.answer +
      (sources
        ? `\n\n---\n\n### 📚 Sources\n${sources}`
        : ""),
  },
]);

    } catch {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "❌ Backend connection failed.",
        },
      ]);
    }

    setLoading(false);
    setQuery("");
  };

const analyzeRepo = async () => {

  let currentOwner = owner;
  let currentRepo = repo;

  if (githubUrl.trim()) {

    const match = githubUrl.match(
      /github\.com\/([^/]+)\/([^/]+)/
    );

    if (!match) {
      alert("Invalid GitHub URL");
      return;
    }

    currentOwner = match[1];
    currentRepo = match[2].replace(".git", "");

    setOwner(currentOwner);
    setRepo(currentRepo);
  }

  if (!currentOwner || !currentRepo) return;

  setLoading(true);

  try {

    const res = await api.post(
      `/github/analyze?owner=${currentOwner}&repo=${currentRepo}`
    );
    const graph = await api.get(
    `/github/dependency-graph?owner=${currentOwner}&repo=${currentRepo}`
    );
    setTree(graph.data);

    const architecture = await api.get(
      `/github/architecture?owner=${currentOwner}&repo=${currentRepo}`
    );
    setGraph(architecture.data);

    const fileRes = await api.post(
    `/github/files?owner=${currentOwner}&repo=${currentRepo}`
    );

    setFiles(fileRes.data.files);

    setAnalysis(res.data.analysis);
    setHealth(res.data.health);

setMessages((prev) => [
  ...prev,
  {
    role: "assistant",
    content:
      "✅ Repository analyzed successfully. You can now ask questions below.",
  },
]);

  } catch {

    setMessages((prev) => [
      ...prev,
      {
        role: "assistant",
        content: "❌ Repository analysis failed.",
      },
    ]);

  }

  setLoading(false);
};

  return (
    <div className="app">
      <div className="glass">
        <div className="header">
          <h1>🚀 Autonomous CTO Agent</h1>
          {owner && repo && (
            <div className="repoStats">

              <div className="statCard">
               <h3>📂 Repository</h3>
               <p>{owner}/{repo}</p>
            </div>

        <div className="statCard">
          <h3>🤖 LLM</h3>
            <p>Gemini</p>
        </div>

        <div className="statCard">
          <h3>🧠 Embeddings</h3>
          <p>Gemini Embedding 001</p>
        </div>

        <div className="statCard">
          <h3>🗄 Vector DB</h3>
          <p>Qdrant</p>
        </div>

        <div className="statCard">
          <h3>📄 Files</h3>
          <p>{files.length}</p>
        </div>

  </div>
)}

          <p>LangGraph • RAG • GitHub MCP • Gemini</p>

          <div className="repoBox">
            <input
              placeholder="Paste GitHub Repository URL"
              value={githubUrl}
              onChange={(e) => setGithubUrl(e.target.value)}
            />
            <input
              placeholder="GitHub Owner"
              value={owner}
              onChange={(e) => setOwner(e.target.value)}
            />

            <input
              placeholder="Repository Name"
              value={repo}
              onChange={(e) => setRepo(e.target.value)}
            />

            <button
             onClick={analyzeRepo}
            disabled={loading}
            >
            {loading ? "⏳ Analyzing Repository..." : "🚀 Analyze Repository"}
            </button>
          </div>
        </div>


        <div className="chatWindow">
          {tree && (
          <FileTree tree={tree} />
        )}
        {graph && (
        <ArchitectureGraph
        graph={graph}
        />
        )}
        {health && (
          <div className="healthCard">
            <h2>📊 Repository Health Score</h2>

            <h3>Overall Score: {health.overall}/100</h3>

            <div className="healthGrid">
              {Object.entries(health.checks).map(([key, value]) => (
                <div key={key} className="healthItem">
                  {value ? "✅" : "❌"} {key}
           </div>
          ))}
      </div>
    </div>
  )}
          {analysis?.length > 0 && (
  <>
    <div className="analysisCard">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeRaw]}
      >
    {
    analysis
      .replace(/#\s*Executive Summary/gi,"# 📌 Summary")
      .replace(/#\s*Repository Health[\s\S]*?(?=#|$)/gi,"")
      .replace(/#\s*Sources[\s\S]*?(?=#|$)/gi,"")
      .replace(/📚\s*Sources[\s\S]*/gi,"")
      .replace(/#\s*Suggested Improvements[\s\S]*?(?=#|$)/gi,"")
      .replace(/#\s*Suggested Questions[\s\S]*?(?=#|$)/gi,"")
      .replace(/#\s*Interview Questions[\s\S]*?(?=#|$)/gi,"")
      .trim()
    }
      </ReactMarkdown>
    </div>

    <div className="suggestions">

      <h3>💡 Suggested Questions</h3>

      <div className="suggestionGrid">

        <button onClick={() => setQuery("Explain the overall architecture")}>
          Architecture
        </button>

        <button onClick={() => setQuery("Which file starts the application?")}>
          Entry Point
        </button>

        <button onClick={() => setQuery("Explain authentication flow")}>
          Authentication
        </button>

        <button onClick={() => setQuery("Explain API flow")}>
          API Flow
        </button>

      </div>

    </div>
  </>
)}
          {messages.map((msg, i) => (
            <div
              key={i}
              className={msg.role === "user" ? "user" : "assistant"}
            >
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                rehypePlugins={[rehypeRaw]}
                components={{
                  code({ inline, className, children, ...props }) {
                    const match = /language-(\w+)/.exec(className || "");

                    return !inline && match ? (
                      <SyntaxHighlighter
                        style={oneDark}
                        language={match[1]}
                        PreTag="div"
                      >
                        {String(children).replace(/\n$/, "")}
                      </SyntaxHighlighter>
                    ) : (
                      <code className={className} {...props}>
                        {children}
                      </code>
                    );
                  },

                  h1: ({ children }) => (
                    <h1 className="md-h1">{children}</h1>
                  ),

                  h2: ({ children }) => (
                    <h2 className="md-h2">{children}</h2>
                  ),

                  h3: ({ children }) => (
                    <h3 className="md-h3">{children}</h3>
                  ),

                  p: ({ children }) => (
                    <p className="md-p">{children}</p>
                  ),

                  ul: ({ children }) => (
                    <ul className="md-ul">{children}</ul>
                  ),

                  ol: ({ children }) => (
                    <ol className="md-ol">{children}</ol>
                  ),

                  blockquote: ({ children }) => (
                    <blockquote className="md-quote">
                      {children}
                    </blockquote>
                  ),

                  table: ({ children }) => (
                    <table className="md-table">{children}</table>
                  ),
                }}
              >
                {msg.content}
              </ReactMarkdown>
            </div>
          ))}

          {loading && (
            <div className="assistant">
              <div className="thinking">

                <div>📥 Downloading Repository...</div>
                <div>📄 Chunking Files...</div>
                <div>🧠 Creating Embeddings...</div>
                <div>🗄 Indexing in Qdrant...</div>
                <div>🔍 Retrieving Context...</div>
                <div>🤖 Gemini is Thinking...</div>
            </div>
          </div>
          )}
        </div>

        <div className="inputBar">
          <input
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            placeholder="Ask about architecture, APIs, code flow, files..."
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                sendMessage();
              }
            }}
          />

          <button onClick={sendMessage}>
            ➤ Send
          </button>
        </div>
      </div>
    </div>
  );
}

export default App;