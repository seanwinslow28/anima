import "../styles/marquee.css";

/**
 * Loading is a skeleton of the *target* screen, never a spinner-in-a-void
 * (states doctrine). A grid of marquee-card shapes for the Dashboard; the
 * pulse rides the ro-pulse primitive so reduced motion stills it.
 */
export function CardGridSkeleton({ count = 6 }: { count?: number }) {
  return (
    <div className="mq-grid" aria-hidden="true" data-testid="dashboard-skeleton">
      {Array.from({ length: count }, (_, i) => (
        <div key={i} className="mq-card mq-card--skeleton">
          <div className="mq-sk mq-sk--name ro-pulse" />
          <div className="mq-sk mq-sk--cta ro-pulse" />
          <div className="mq-sk mq-sk--meta ro-pulse" />
        </div>
      ))}
    </div>
  );
}
