import "./FileTree.css";

function Tree({ data, level = 0 }) {
  return (
    <>
      {Object.entries(data).map(([key, value]) => {
        // Render files
        if (key === "__files__" && Array.isArray(value)) {
          return value.map((file) => (
            <div
              key={`${level}-${file}`}
              style={{
                paddingLeft: `${level * 20}px`,
                margin: "4px 0",
              }}
            >
              📄 {file}
            </div>
          ));
        }

        // Render folders
        return (
          <div key={key}>
            <div
              style={{
                paddingLeft: `${level * 20}px`,
                margin: "6px 0",
                fontWeight: "bold",
              }}
            >
              📁 {key}
            </div>

            {typeof value === "object" &&
              value !== null && (
                <Tree
                  data={value}
                  level={level + 1}
                />
              )}
          </div>
        );
      })}
    </>
  );
}

export default function FileTree({ tree }) {
  if (!tree) return null;

  return (
    <div className="fileTree">
      <h2>📂 Repository Files</h2>

      <Tree data={tree} />
    </div>
  );
}