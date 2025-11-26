# Medical Assistant Chatbot Design Guidelines

## Design Approach: Reference-Based
Drawing inspiration from modern healthcare applications like Headspace, Calm, and contemporary telehealth platforms that use warm, approachable aesthetics. The design prioritizes trust, warmth, and clarity while maintaining medical professionalism.

## Typography

**Font Stack:**
- Primary: Inter or DM Sans (clean, modern sans-serif for UI elements)
- Accent: Sora or Plus Jakarta Sans (softer, rounded for headers and warmth)

**Hierarchy:**
- Main header: 2xl (font-bold)
- Chat messages: base (font-normal for assistant, font-medium for user)
- Sidebar labels: sm (font-medium)
- Meta information: xs (font-normal)
- Button text: sm (font-semibold)

## Layout System

**Spacing Primitives:** Use Tailwind units of 2, 4, 6, and 8 consistently
- Component padding: p-4, p-6
- Section margins: mb-4, mb-6, mb-8
- Icon spacing: mr-2, ml-2
- Container gaps: gap-4, gap-6

**Grid Structure:**
- Main container: max-w-5xl mx-auto with p-6
- Sidebar: Fixed width 280px (desktop), full-width drawer (mobile)
- Chat area: flex-1 with proper overflow handling

## Component Library

### Header
Full-width gradient banner with:
- Medical icon (stethoscope) on left
- App title centered with heartbeat animation icon
- Theme toggle (sun/moon icon) on right
- Height: h-16 with shadow-md

### Sidebar (Desktop: Fixed Panel, Mobile: Drawer)
Contains three sections with dividers:
1. **Session Info Card**: Rounded card (rounded-lg) displaying session ID and message count with medical cross icon
2. **Controls**: Developer mode toggle switch with label, Clear chat button (full-width, rounded-md)
3. **Theme Switcher**: Light/Dark mode toggle with smooth transition

### Chat Interface
**Message Container**: Scrollable area with pb-24 to prevent input overlap

**User Messages:**
- Right-aligned with flex justify-end
- Rounded bubble: rounded-2xl rounded-br-sm
- Avatar (U initial) in circular badge (w-10 h-10)
- Max width: max-w-lg
- Shadow: shadow-md

**AI Messages:**
- Left-aligned
- Rounded bubble: rounded-2xl rounded-bl-sm
- Stethoscope icon in circular badge
- Max width: max-w-2xl
- Border with shadow-sm
- "Thinking" state: Pulsing animation with three dots

**Developer Mode Meta:**
- Collapsible accordion under AI messages
- Monospace font (font-mono, text-xs)
- Subtle border-l-2 with pl-3

### Chat Input
- Fixed bottom position with backdrop-blur
- Height: h-14
- Rounded: rounded-full
- Send button: Circular (w-10 h-10) with paper plane icon
- Focus ring on input

### Buttons
- Primary CTA: rounded-lg, px-6, py-2.5, font-semibold with shadow-sm
- Secondary: outlined variant with border-2
- Icon buttons: p-2, rounded-full
- All implement standard hover/active states (scale-105, shadow-lg on hover)

## Theme System Architecture

### Light Mode Structure
- Background: Warm off-white gradient
- Message bubbles: Soft shadows with warm tones
- Sidebar: Light card background
- Text: Deep warm grays

### Dark Mode (Rose-Gold Night)
- Background: Deep burgundy gradient
- Message bubbles: Elevated cards with gold accents
- Sidebar: Dark card with rose highlights
- Text: Warm light tones with high contrast
- Glowing accents on interactive elements

**Theme Toggle:** Smooth transition-all duration-300 on theme change, persist preference in localStorage

## Icons & Assets

**Icon Library:** Heroicons via CDN
- Stethoscope/medical icon for AI avatar
- User circle for user avatar
- Sun/moon for theme toggle
- Heart with pulse animation for header
- Paper airplane for send button
- Trash icon for clear chat
- Chevron for collapsible sections

**Medical Accents:**
- Subtle heartbeat line animation in header (CSS animation, keyframes)
- Pulsing dot indicator during "thinking" state
- Medical cross icon in session info card

## Animations

**Strategic Use Only:**
- Heartbeat pulse in header (subtle, 2s loop)
- Message appearance: slide-in from right (user) / left (AI) with fade
- Thinking indicator: 3-dot pulse animation
- Theme transition: smooth 300ms fade
- Button hover: scale-105 transform

## Responsive Behavior

**Desktop (lg+):**
- Sidebar visible as fixed panel
- Chat centered with max-w-5xl
- Multi-line input allowed

**Tablet (md):**
- Sidebar as slide-out drawer
- Hamburger menu icon in header

**Mobile (base):**
- Full-width chat
- Compact header (h-14)
- Single-line input with send button
- Avatar sizes reduced (w-8 h-8)

## Images

No hero images required. Medical iconography and SVG illustrations only:
- Optional: Subtle medical-themed background pattern (ECG line, subtle in header gradient area)
- Avatar placeholders use icon-based approach, not photos