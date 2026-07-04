/**
 * Loading is a skeleton of the *target* screen, never a spinner-in-a-void
 * (states doctrine). A grid of card-shaped placeholders for the Dashboard.
 */
export function CardGridSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="grid" aria-hidden="true" data-testid="dashboard-skeleton">
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className="runcard runcard--skeleton">
          <div className="sk-line sk-line--title" />
          <div className="sk-line sk-line--id" />
          <div className="sk-line sk-line--cta" />
        </div>
      ))}
    </div>
  );
}
