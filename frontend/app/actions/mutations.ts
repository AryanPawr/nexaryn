"use server";

import { revalidatePath } from "next/cache";
import { approveAction, denyAction } from "@/lib/api";

function actionId(formData: FormData): string {
  const value = formData.get("action_id");
  if (typeof value !== "string" || value.length === 0) {
    throw new Error("action_id is required.");
  }
  return value;
}

export async function approveActionForm(formData: FormData) {
  await approveAction(actionId(formData));
  revalidatePath("/actions");
}

export async function denyActionForm(formData: FormData) {
  await denyAction(actionId(formData));
  revalidatePath("/actions");
}
