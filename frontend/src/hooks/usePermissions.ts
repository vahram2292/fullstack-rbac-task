import type { Permission } from "@/client"
import useAuth from "./useAuth"

/**
 * What the current user may do, as reported by the API (`user.permissions`).
 * The UI never maps roles to permissions itself; the backend is the only
 * place that knows which role grants what.
 */
const usePermissions = () => {
  const { user } = useAuth()

  const can = (permission: Permission): boolean =>
    user?.permissions.includes(permission) ?? false

  return { can, isLoaded: user != null }
}

export default usePermissions
