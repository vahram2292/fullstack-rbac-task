import { BarChart3, Briefcase, Home, Users } from "lucide-react"

import type { Permission } from "@/client"
import { SidebarAppearance } from "@/components/Common/Appearance"
import { Logo } from "@/components/Common/Logo"
import {
  Sidebar,
  SidebarContent,
  SidebarFooter,
  SidebarHeader,
} from "@/components/ui/sidebar"
import useAuth from "@/hooks/useAuth"
import usePermissions from "@/hooks/usePermissions"
import { type Item, Main } from "./Main"
import { User } from "./User"

type NavItem = Item & { requiredPermission?: Permission }

const navItems: NavItem[] = [
  { icon: Home, title: "Dashboard", path: "/" },
  { icon: Briefcase, title: "Items", path: "/items" },
  {
    icon: BarChart3,
    title: "Metrics",
    path: "/metrics",
    requiredPermission: "metrics:read",
  },
  {
    icon: Users,
    title: "Users",
    path: "/admin",
    requiredPermission: "users:read",
  },
]

export function AppSidebar() {
  const { user: currentUser } = useAuth()

  const { can } = usePermissions()

  const items = navItems.filter(
    ({ requiredPermission }) => !requiredPermission || can(requiredPermission),
  )

  return (
    <Sidebar collapsible="icon">
      <SidebarHeader className="px-4 py-6 group-data-[collapsible=icon]:px-0 group-data-[collapsible=icon]:items-center">
        <Logo variant="responsive" />
      </SidebarHeader>
      <SidebarContent>
        <Main items={items} />
      </SidebarContent>
      <SidebarFooter>
        <SidebarAppearance />
        <User user={currentUser} />
      </SidebarFooter>
    </Sidebar>
  )
}

export default AppSidebar
