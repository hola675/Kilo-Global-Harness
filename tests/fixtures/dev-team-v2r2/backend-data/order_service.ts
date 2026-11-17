type Order = {
  id: string
  status: "new" | "processed"
  viewCount: number
}

interface Store {
  find(id: string): Promise<Order | null>
  save(order: Order): Promise<void>
}

export async function getOrder(store: Store, id: string) {
  const order = await store.find(id)
  if (!order) return null

  order.viewCount += 1
  order.status = "processed"
  await store.save(order)

  return order
}
