"use client";

import { motion, useReducedMotion } from "framer-motion";
import type { ReactNode } from "react";

type PageTransitionProps = {
  children: ReactNode;
};

/**
 * Subtle page entrance. Uses initial={false} so content is never hidden
 * when animation fails (browser themes, hydration, or reduced motion edge cases).
 */
export function PageTransition({ children }: PageTransitionProps) {
  const shouldReduceMotion = useReducedMotion();

  if (shouldReduceMotion) {
    return <div className="min-h-[1px]">{children}</div>;
  }

  return (
    <motion.div
      initial={false}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.25, ease: "easeOut" }}
      className="min-h-[1px]"
    >
      {children}
    </motion.div>
  );
}
