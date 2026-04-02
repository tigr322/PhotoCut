export type ToastType = 'success' | 'error' | 'info'

export interface ToastMessage {
  id: number
  type: ToastType
  message: string
}

export const useToast = () => {
  const toasts = useState<ToastMessage[]>('toasts', () => [])

  const push = (message: string, type: ToastType = 'info') => {
    const item: ToastMessage = {
      id: Date.now() + Math.floor(Math.random() * 1000),
      message,
      type,
    }

    toasts.value = [item, ...toasts.value]
    setTimeout(() => {
      toasts.value = toasts.value.filter((toast) => toast.id !== item.id)
    }, 4000)
  }

  return { toasts, push }
}
