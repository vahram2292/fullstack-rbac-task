import type { Role } from "@/client"

// Typed as Record<Role, …> so adding a role in the API without a label
// here fails the build.
export const ROLE_LABELS: Record<Role, string> = {
  admin: "Admin",
  manager: "Manager",
  member: "Member",
}

export const ROLES = Object.keys(ROLE_LABELS) as Role[]
