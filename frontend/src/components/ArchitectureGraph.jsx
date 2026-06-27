import React from "react";
import ReactFlow, {
  Background,
  Controls,
  MiniMap,
} from "reactflow";

import "reactflow/dist/style.css";

export default function ArchitectureGraph({
  graph,
}) {

  if (!graph) return null;

  const nodes = graph.nodes.map((n, index) => ({
    id: n.id,
    data: {
      label: n.id.split("/").pop(),
    },
    position: {
      x: (index % 5) * 220,
      y: Math.floor(index / 5) * 120,
    },
  }));

  const edges = graph.edges.map((e, i) => ({
    id: String(i),
    source: e.source,
    target: e.target,
    animated: true,
  }));

  return (
    <div
      style={{
        height: 600,
        marginTop: 25,
        borderRadius: 20,
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