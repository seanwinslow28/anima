import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

/**
 * The lit page's prose renderer: Maya's / Sam's / Bea's markdown as real
 * elements (react-markdown + remark-gfm — parser-only, no HTML passthrough,
 * so daemon-served markdown can't inject markup). Document headings are
 * demoted one level (h1->h2 … h5->h6): the GateShell's gate title is the
 * screen's only h1 (the a11y contract).
 */
export function Markdown({ text }: { text: string }) {
  return (
    <div className="gate-prose">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        components={{
          h1: "h2",
          h2: "h3",
          h3: "h4",
          h4: "h5",
          h5: "h6",
        }}
      >
        {text}
      </ReactMarkdown>
    </div>
  );
}
