import { useSuspenseQuery } from "@tanstack/react-query"
import { createFileRoute } from "@tanstack/react-router"
import { Suspense } from "react"

import { MetricsService } from "@/client"
import RequirePermission from "@/components/Common/RequirePermission"
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card"
import { Skeleton } from "@/components/ui/skeleton"
import { ROLE_LABELS, ROLES } from "@/lib/roles"

export const Route = createFileRoute("/_layout/metrics")({
  component: Metrics,
  head: () => ({
    meta: [
      {
        title: "Metrics - FastAPI Template",
      },
    ],
  }),
})

function StatCard({ title, value }: { title: string; value: number }) {
  return (
    <Card>
      <CardHeader>
        <CardTitle className="text-sm font-medium text-muted-foreground">
          {title}
        </CardTitle>
      </CardHeader>
      <CardContent>
        <span className="text-3xl font-bold">{value}</span>
      </CardContent>
    </Card>
  )
}

function MetricsContent() {
  const { data: metrics } = useSuspenseQuery({
    queryKey: ["metrics"],
    queryFn: async () => (await MetricsService.readMetrics()).data,
  })

  return (
    <div className="flex flex-col gap-4">
      <div className="grid gap-4 sm:grid-cols-3">
        <StatCard title="Total users" value={metrics.total_users} />
        <StatCard title="Active users" value={metrics.active_users} />
        <StatCard title="Total items" value={metrics.total_items} />
      </div>
      <h2 className="text-lg font-semibold mt-2">Users by role</h2>
      <div className="grid gap-4 sm:grid-cols-3">
        {ROLES.map((role) => (
          <StatCard
            key={role}
            title={ROLE_LABELS[role]}
            value={metrics.users_by_role[role] ?? 0}
          />
        ))}
      </div>
    </div>
  )
}

function Metrics() {
  return (
    <RequirePermission permission="metrics:read">
      <div className="flex flex-col gap-6">
        <div>
          <h1 className="text-2xl font-bold tracking-tight">Metrics</h1>
          <p className="text-muted-foreground">
            A snapshot of how the application is being used
          </p>
        </div>
        <Suspense fallback={<Skeleton className="h-32 w-full" />}>
          <MetricsContent />
        </Suspense>
      </div>
    </RequirePermission>
  )
}
