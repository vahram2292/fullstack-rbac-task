import { expect, type Page, test } from "@playwright/test"
import type { Role } from "../src/client"
import { createUserWithRole } from "./utils/adminApi"
import { randomEmail, randomPassword } from "./utils/random"
import { logInUser } from "./utils/user"

test.use({ storageState: { cookies: [], origins: [] } })

async function logInAsNewUser(page: Page, role: Role) {
  const email = randomEmail()
  const password = randomPassword()
  await createUserWithRole({ email, password, role })
  await logInUser(page, email, password)
}

test.describe("Manager", () => {
  test.beforeEach(async ({ page }) => {
    await logInAsNewUser(page, "manager")
  })

  test("sees the Users and Metrics links", async ({ page }) => {
    await expect(page.getByRole("link", { name: "Users" })).toBeVisible()
    await expect(page.getByRole("link", { name: "Metrics" })).toBeVisible()
  })

  test("can view the users list but not change it", async ({ page }) => {
    await page.goto("/admin")

    await expect(page.getByRole("heading", { name: "Users" })).toBeVisible()
    await expect(page.getByText("View user accounts and roles")).toBeVisible()
    await expect(page.getByRole("row").nth(1)).toBeVisible()
    await expect(page.getByRole("button", { name: "Add User" })).toHaveCount(0)
    // Row action menus (edit / delete) are the only buttons inside the table
    await expect(page.locator("tbody button")).toHaveCount(0)
  })

  test("can view metrics", async ({ page }) => {
    await page.goto("/metrics")

    await expect(page.getByRole("heading", { name: "Metrics" })).toBeVisible()
    await expect(page.getByText("Total users")).toBeVisible()
  })
})

test.describe("Member", () => {
  test.beforeEach(async ({ page }) => {
    await logInAsNewUser(page, "member")
  })

  test("does not see the Users and Metrics links", async ({ page }) => {
    await expect(page.getByRole("link", { name: "Items" })).toBeVisible()
    await expect(page.getByRole("link", { name: "Users" })).toHaveCount(0)
    await expect(page.getByRole("link", { name: "Metrics" })).toHaveCount(0)
  })

  test("sees Access denied on the metrics page and stays logged in", async ({
    page,
  }) => {
    await page.goto("/metrics")

    await expect(page.getByTestId("forbidden")).toBeVisible()
    await expect(page.getByText("Total users")).toHaveCount(0)

    await page.getByRole("link", { name: "Back to dashboard" }).click()
    await expect(
      page.getByText("Welcome back, nice to see you again!"),
    ).toBeVisible()
  })
})
