import { Link } from "@tanstack/react-router"
import { ShieldAlert } from "lucide-react"

import { Button } from "@/components/ui/button"

const Forbidden = () => {
  return (
    <div
      className="flex flex-col items-center justify-center text-center py-16"
      data-testid="forbidden"
    >
      <div className="rounded-full bg-muted p-4 mb-4">
        <ShieldAlert className="size-8 text-muted-foreground" />
      </div>
      <h1 className="text-2xl font-bold tracking-tight">Access denied</h1>
      <p className="text-muted-foreground mt-2 max-w-md">
        Your account doesn't have permission to view this page. If you think you
        should have access, ask an administrator.
      </p>
      <Link to="/">
        <Button className="mt-6">Back to dashboard</Button>
      </Link>
    </div>
  )
}

export default Forbidden
