import { ErrorPageShell } from "@/components/errors/ErrorPageShell";

export default function NotFound() {
  return (
    <ErrorPageShell
      statusCode="404"
      title="Page not found"
      description="The page you requested does not exist or may have been moved. Use the navigation below or return to the homepage."
    />
  );
}
