import { PageHeaderSkeleton, SectionSkeleton } from "@/components/ui/Skeleton";

export default function Loading() {
  return (
    <>
      <PageHeaderSkeleton />
      <SectionSkeleton cards={3} />
      <SectionSkeleton cards={6} variant="muted" />
    </>
  );
}
