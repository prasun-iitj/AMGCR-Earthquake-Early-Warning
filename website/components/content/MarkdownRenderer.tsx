import Link from "next/link";
import ReactMarkdown from "react-markdown";
import rehypeAutolinkHeadings from "rehype-autolink-headings";
import rehypeRaw from "rehype-raw";
import rehypeSanitize, { defaultSchema } from "rehype-sanitize";
import rehypeSlug from "rehype-slug";
import remarkGfm from "remark-gfm";
import { isExternalHref, rewriteMarkdownHref } from "@/lib/content/links";

const sanitizeSchema = {
  ...defaultSchema,
  attributes: {
    ...defaultSchema.attributes,
    div: [...(defaultSchema.attributes?.div ?? []), "align"],
  },
};

type MarkdownRendererProps = {
  content: string;
  sourcePath: string;
};

export function MarkdownRenderer({
  content,
  sourcePath,
}: MarkdownRendererProps) {
  return (
    <div className="doc-prose">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[
          rehypeRaw,
          [rehypeSanitize, sanitizeSchema],
          rehypeSlug,
          [
            rehypeAutolinkHeadings,
            {
              behavior: "wrap",
              properties: { className: ["anchor-link"] },
            },
          ],
        ]}
        components={{
          a: ({ href, children, ...props }) => {
            const resolved =
              rewriteMarkdownHref(href, sourcePath) ?? href ?? "#";
            const external = isExternalHref(resolved);

            if (external) {
              return (
                <a
                  href={resolved}
                  target="_blank"
                  rel="noopener noreferrer"
                  {...props}
                >
                  {children}
                </a>
              );
            }

            if (resolved.startsWith("#")) {
              return (
                <a href={resolved} {...props}>
                  {children}
                </a>
              );
            }

            return (
              <Link href={resolved} {...props}>
                {children}
              </Link>
            );
          },
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
