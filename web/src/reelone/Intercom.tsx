import { useEffect, useRef, useState } from "react";

const INTERCOM_EVENT = "reelone:intercom";
export const INTERCOM_DISMISS_MS = 2600;

type IntercomDetail = { message: string };

/** Call the booth's shared, route-persistent intercom line. */
export function callIntercom(message: string) {
  window.dispatchEvent(
    new CustomEvent<IntercomDetail>(INTERCOM_EVENT, { detail: { message } }),
  );
}

/**
 * A transient booth acknowledgment, mounted once by BoothShell so a gate can
 * advance without cutting off its own reply. It never takes focus or blocks
 * the decision terminal underneath it.
 */
export function Intercom() {
  const [message, setMessage] = useState("");
  const dismiss = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    const onCall = (event: Event) => {
      const next = (event as CustomEvent<IntercomDetail>).detail?.message;
      if (!next) return;
      if (dismiss.current !== null) clearTimeout(dismiss.current);
      setMessage(next);
      dismiss.current = setTimeout(() => {
        setMessage("");
        dismiss.current = null;
      }, INTERCOM_DISMISS_MS);
    };
    window.addEventListener(INTERCOM_EVENT, onCall);
    return () => {
      window.removeEventListener(INTERCOM_EVENT, onCall);
      if (dismiss.current !== null) clearTimeout(dismiss.current);
    };
  }, []);

  return (
    <div
      className={message ? "ro-intercom ro-intercom--called" : "ro-intercom"}
      role="status"
      aria-live="polite"
      aria-atomic="true"
    >
      {message}
    </div>
  );
}
