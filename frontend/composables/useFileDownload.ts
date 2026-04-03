import type { Job } from '~/types'

const parseFilenameFromContentDisposition = (value: string | null): string | null => {
  if (!value) return null

  const utf8Match = value.match(/filename\*=UTF-8''([^;]+)/i)
  if (utf8Match?.[1]) {
    try {
      return decodeURIComponent(utf8Match[1])
    } catch {
      return utf8Match[1]
    }
  }

  const asciiMatch = value.match(/filename="?([^";]+)"?/i)
  return asciiMatch?.[1] ?? null
}

export const useFileDownload = () => {
  const config = useRuntimeConfig()
  const auth = useAuthStore()

  const downloadResultFile = async (job: Job): Promise<void> => {
    if (!job.result_url) {
      throw new Error('File is not ready yet')
    }
    if (!auth.token) {
      throw new Error('Authentication required')
    }

    const response = await fetch(`${config.public.apiBase}${job.result_url}`, {
      method: 'GET',
      headers: {
        Authorization: `Bearer ${auth.token}`,
      },
    })

    if (!response.ok) {
      let message = 'Failed to download file'
      try {
        const payload = (await response.json()) as { detail?: string }
        if (payload.detail) message = payload.detail
      } catch {
        // keep default message
      }
      throw new Error(message)
    }

    const blob = await response.blob()
    const contentDisposition = response.headers.get('content-disposition')
    const filename = parseFilenameFromContentDisposition(contentDisposition) ?? `result-${job.id}.png`

    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')
    link.href = url
    link.download = filename
    document.body.appendChild(link)
    link.click()
    link.remove()
    URL.revokeObjectURL(url)
  }

  return { downloadResultFile }
}
