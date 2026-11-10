import type { ReactNode } from "react"

import type { Permission } from "@/client"
import usePermissions from "@/hooks/usePermissions"
import Forbidden from "./Forbidden"

interface RequirePermissionProps {
  permission: Permission
  children: ReactNode
}

/** Renders a page only for users holding `permission`; others see "Access denied". */
const RequirePermission = ({
  permission,
  children,
}: RequirePermissionProps) => {
  const { can, isLoaded } = usePermissions()

  if (!isLoaded) {
    return null
  }
  return can(permission) ? children : <Forbidden />
}

export default RequirePermission
