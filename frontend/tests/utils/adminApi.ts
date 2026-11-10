import { LoginService, type Role, UsersService } from "../../src/client"
import { client } from "../../src/client/client.gen"
import { firstSuperuser, firstSuperuserPassword } from "../config.ts"

client.setConfig({
  baseURL: `${process.env.VITE_API_URL}`,
})

/** Creates a user with the given role through the real API, as the first admin. */
export const createUserWithRole = async ({
  email,
  password,
  role,
}: {
  email: string
  password: string
  role: Role
}) => {
  const { data: token } = await LoginService.loginAccessToken({
    body: { username: firstSuperuser, password: firstSuperuserPassword },
  })
  const response = await UsersService.createUser({
    body: { email, password, role, is_active: true },
    headers: { Authorization: `Bearer ${token.access_token}` },
  })
  return response.data
}
