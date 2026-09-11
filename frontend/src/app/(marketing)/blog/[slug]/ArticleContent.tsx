'use client';

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import rehypeSlug from 'rehype-slug';
import rehypeRaw from 'rehype-raw';

interface ArticleContentProps {
  content: string;
}

export default function ArticleContent({ content }: ArticleContentProps) {
  return (
    <div className="prose prose-invert prose-slate max-w-none
      prose-headings:font-display prose-headings:text-slate-50 prose-headings:font-bold
      prose-h2:text-2xl prose-h2:sm:text-3xl prose-h2:mt-12 prose-h2:mb-6 prose-h2:border-b prose-h2:border-white/10 prose-h2:pb-4
      prose-h3:text-xl prose-h3:sm:text-2xl prose-h3:mt-8 prose-h3:mb-4
      prose-h4:text-lg prose-h4:mt-6 prose-h4:mb-3
      prose-p:text-slate-300 prose-p:leading-relaxed prose-p:text-base
      prose-a:text-teal-400 prose-a:no-underline hover:prose-a:text-teal-300 prose-a:transition-colors
      prose-strong:text-slate-100 prose-strong:font-semibold
      prose-em:text-slate-300
      prose-code:text-teal-300 prose-code:bg-teal-500/10 prose-code:px-1.5 prose-code:py-0.5 prose-code:rounded prose-code:text-sm prose-code:font-normal prose-code:before:content-none prose-code:after:content-none
      prose-pre:bg-slate-900/80 prose-pre:border prose-pre:border-white/10 prose-pre:rounded-xl
      prose-blockquote:border-teal-500/50 prose-blockquote:bg-teal-500/5 prose-blockquote:rounded-r-xl prose-blockquote:py-1 prose-blockquote:text-slate-300 prose-blockquote:not-italic
      prose-ul:text-slate-300 prose-ol:text-slate-300
      prose-li:text-slate-300 prose-li:marker:text-teal-400
      prose-hr:border-white/10
      prose-table:text-sm
      prose-th:text-slate-200 prose-th:font-display prose-th:font-semibold prose-th:bg-white/5 prose-th:px-4 prose-th:py-3
      prose-td:text-slate-300 prose-td:px-4 prose-td:py-3 prose-td:border-white/10
      prose-tr:border-white/10
      prose-img:rounded-xl prose-img:border prose-img:border-white/10
    ">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeSlug, rehypeRaw]}
        components={{
          h1: ({ children, ...props }) => <h2 {...props}>{children}</h2>,
        }}
      >
        {content}
      </ReactMarkdown>
    </div>
  );
}
