import type { Role } from "@/client"

// Typed as Record<Role, …> so adding a role in the API without a label
// here fails the build.
export const ROLE_LABELS: Record<Role, string> = {
  admin: "Admin",
  manager: "Manager",
  member: "Member",
}

export const ROLE_BADGE_VARIANTS: Record<Role, "default" | "secondary"> = {
  admin: "default",
  manager: "default",
  member: "secondary",
}

export const ROLES = Object.keys(ROLE_LABELS) as Role[]
