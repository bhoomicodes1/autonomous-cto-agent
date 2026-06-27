import React from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
} from "reactflow";

import "reactflow/dist/style.css";

export default function ArchitectureGraph({ graph }) {

  console.log("GRAPH RECEIVED:", graph);

  if (!graph) return null;

  const nodeList = graph.nodes || graph.vertices || [];
  const edgeList = graph.edges || graph.links || [];

  const nodes = nodeList.map((n, index) => ({
    id: String(n.id),
    data: {
      label: String(n.id).split("/").pop(),
    },
    position: {
      x: (index % 5) * 220,
      y: Math.floor(index / 5) * 120,
    },
  }));

  const edges = edgeList.map((e, index) => ({
    id: String(index),
    source: String(e.source),
    target: String(e.target),
    animated: true,
  }));

  return (
    <div
      style={{
        width: "100%",
        height: "600px",
        marginTop: "20px",
        border: "1px solid #333",
        borderRadius: "16px",
        overflow: "hidden",
      }}
    >
      <ReactFlow
        nodes={nodes}
        edges={edges}
        fitView
      >
        <MiniMap />
        <Controls />
        <Background />
      </ReactFlow>
    </div>
  );
}