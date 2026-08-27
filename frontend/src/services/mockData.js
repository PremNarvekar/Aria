export const MOCK_SESSIONS = [
  {
    id: "session_001",
    question: "How is NVIDIA positioned in the AI infrastructure market?",
    createdAt: "2026-08-25T14:30:00Z",
    status: "complete", // 'empty', 'researching', 'complete', 'error'
    summary: "NVIDIA dominates the AI infrastructure market through its full-stack approach, combining GPU hardware (like the H100 and upcoming Blackwell), proprietary CUDA software, and high-speed networking (InfiniBand). This creates a highly integrated ecosystem that makes it exceptionally difficult for competitors like AMD or Intel to displace them in data centers.",
    findings: [
      "NVIDIA holds an estimated 80-95% market share in AI data center GPUs.",
      "CUDA's 15-year head start constitutes NVIDIA's strongest defensive moat.",
      "The shift towards system-level sales (GB200 NVL72) increases margins and lock-in."
    ],
    claims: [
      {
        id: "c1",
        text: "NVIDIA's CUDA ecosystem has become a major component of its AI computing platform.",
        evidence: "CUDA provides developers with direct access to GPU virtual instruction sets and parallel computational elements, resulting in a software lock-in that competitors have struggled to break.",
        sourceId: "src_nvidia_1"
      },
      {
        id: "c2",
        text: "System-level architecture is replacing individual GPU sales.",
        evidence: "NVIDIA's strategy has shifted from selling discrete GPUs to entire server racks (e.g., the GB200 NVL72) containing integrated networking and CPUs.",
        sourceId: "src_wsj_1"
      }
    ],
    sources: [
      {
        id: "src_nvidia_1",
        title: "NVIDIA Data Center Platform",
        domain: "nvidia.com",
        url: "https://www.nvidia.com/en-us/data-center/",
        relevance: 0.98,
        description: "NVIDIA develops accelerated computing platforms for AI and high-performance computing.",
        type: "Company Documentation"
      },
      {
        id: "src_wsj_1",
        title: "How Nvidia Built a Moat Around AI",
        domain: "wsj.com",
        url: "https://www.wsj.com/tech/nvidia-ai-moat-software",
        relevance: 0.92,
        description: "Analysis of NVIDIA's shift towards full-stack data center solutions and the impact on the broader semiconductor industry.",
        type: "News / Analysis"
      }
    ],
    report: `
## Executive Summary
NVIDIA is currently the undisputed leader in the AI infrastructure market. Their dominance is not merely a product of superior silicon, but rather a deeply entrenched, vertically integrated ecosystem that spans hardware, software, and networking.

## The Full-Stack Strategy
Unlike traditional semiconductor companies that sell components, NVIDIA sells an entire data center architecture. 
- **Silicon:** The H100 Hopper and upcoming Blackwell architectures offer unprecedented compute density for transformer models.
- **Software:** The CUDA platform, cultivated over 15 years, is the lingua franca of AI research. Most major AI frameworks (PyTorch, TensorFlow) are heavily optimized for CUDA.
- **Networking:** Through the acquisition of Mellanox, NVIDIA controls InfiniBand, a critical technology for linking tens of thousands of GPUs together efficiently.

## Competitive Landscape
While competitors like AMD (with MI300X) and Intel are attempting to challenge NVIDIA's hardware performance, they face significant hurdles in software maturity (ROCm vs CUDA). Cloud providers (AWS Trainium, Google TPU, Microsoft Maia) are developing custom silicon to reduce reliance on NVIDIA, which represents the most significant long-term threat to NVIDIA's margins.

## Future Outlook
NVIDIA is aggressively moving up the stack, providing foundation models (NIMs) and AI foundry services. This indicates a transition from an infrastructure provider to an AI platform company.
    `,
    followUpHistory: [
      {
        id: "msg_1",
        role: "user",
        text: "Who are its biggest competitors?"
      },
      {
        id: "msg_2",
        role: "assistant",
        text: "NVIDIA's primary competitors fall into two categories:\n\n1. **Merchant Silicon Providers:** AMD is the closest direct competitor with its MI300X accelerators. Intel is also competing with its Gaudi 3 chips.\n2. **Cloud Service Providers (Hyperscalers):** Google (TPU), Amazon (Trainium/Inferentia), and Microsoft (Maia) are designing custom ASICs tailored for their own data centers to reduce reliance on NVIDIA's expensive hardware.",
        sources: ["src_wsj_1"]
      }
    ]
  },
  {
    id: "session_002",
    question: "Analyze India's AI semiconductor ecosystem.",
    createdAt: "2026-08-26T09:15:00Z",
    status: "complete",
    summary: "India is actively building a semiconductor ecosystem through heavy government subsidies (India Semiconductor Mission) and international partnerships. While currently lacking advanced fab capabilities, it is rapidly growing in IC design, testing, and packaging (OSAT), positioning itself as an alternative node in the global supply chain.",
    findings: [],
    claims: [],
    sources: [],
    report: "Report generation complete.",
    followUpHistory: []
  }
];
