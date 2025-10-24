export const Container = ({ children }) => (
  <div className="mx-auto max-w-5xl px-4 py-8">{children}</div>
);

export const PageHeading = ({ title, subtitle }) => (
  <header className="mb-6">
    <h1 className="text-3xl font-semibold text-slate-900">{title}</h1>
    {subtitle && <p className="mt-2 text-slate-600">{subtitle}</p>}
  </header>
);
