# AIVideo

This repository contains a set of scripts for fully automating the AI video production process, including automatic publishing to platforms like official accounts.

[English](README_en.md) | [中文](README_zh.md)

Here are some thoughts on building this project:

Overall Process
LLM Generates Video Prompt -> Video Generation Model -> Local Background Music Matching (based on text prompt) -> Publishing
macbook -> Get TP from LLM Server -> macbook -> Send TP to T2V Model -> Download video to macbook -> Search local library for corresponding audio -> Match and synthesize corresponding video -> Local video storage & publish to multiple platforms.

Registration and Deployment

Tiktok / Douyin (ByteDance ecosystem including Xigua Video) Requires administrator approval.

Bilibili Requires verification.

Youtube Already working.

Kuaishou

Video titles for Chinese platforms need localization.

2.1 text2video: Generate imaginative scenes that don't exist in reality.

Effect Validation

Call Zhipu GLM API to generate semantic prompts.

Call to generate videos:

Highly imaginative videos combining popular online memes.

2.2 image2video:

Video Types: (Can register multiple accounts using different emails)

Suggestive content: Large-scale real beauties, anime beauties, micro-movements - dancing. Some models may refuse to generate these.

Fighting, Kung Fu.

TP -> Diffusion model -> Video.

Historical progress type?

Highly imaginative type?

Real scenes transformed into imaginary virtual scenes.

Implementation Plan

Requirements: Write Python scripts, add Chinese comments, run in a mac environment. Automate the entire process from video generation to publishing. Text prompts call language model API, video generation models are cloud-based.

Call Language Model to Automatically Generate text prompt: Requires being highly creative and imaginative, with wild ideas. To be published on short video platforms, they must be able to attract subscriptions and likes. The video thumbnail on video platforms is usually the first frame of the video.

Path Parameter Requirements:

Save generated videos in the /Users/truman/AIGC/Video folder.

Naming rule: V + Date + Code (Example: V20251230000001).

Automatic Video Publishing Platforms:

Youtube @VideoAIGC account.

Tiktok @videoaigc account.

Model Call: Pika series models.

Video Content Prompt Generation: Generated via Zhipu GLM-4.

Background Music: Automatically add background music after downloading the generated video.

Build Background Music Library

5-second Background Music Library: Categorized by emotion.

10-second Library: To be done later.

Video Generation Models

Most can directly do T2V. Some allow adding Image prompts to improve effects.

Main:

Pika Series: 0.5 seconds. Recommended. I2V, T2V, I+T2V. Second cheapest recommended, easy to deploy.

Keling: 1.6. Recommended. Provides T2V, T+(1-4)I2V multiple interfaces. Only use 5 seconds. Cheapest. Requires domestic mobile phone login. API access is expensive.

Backup:

Runway Gen-3: Highest quality (Gen-2 has Western bias due to training data). 5 RMB per video is too expensive, not recommended.

T2V: Tencent Hunyuan: https://aivideo.hunyuan.tencent.com/. Primarily horizontal, generated vertical videos look like two horizontal ones stitched together. Picture quality needs improvement, action range needs consideration. API: https://cloud.tencent.com/document/product/1729. 5 seconds. No API call interface.

I2V, T2V (T2I2V): Stable Video Diffusion: Only 4 seconds. Easily refuses to generate large-scale content, not recommended. https://www.stablevideo.com/generate.

T2V: Meta MovieGen: Not yet publicly available, will try later.

T2V: Google Veo2: Not yet publicly available, will try later.

T2V: Sora V2: 20/200$, bundled with GPT, Tier 1. But not the best effect, not cost-effective. Can try.

T2V: ModelScope Text to Video: Clarity is not good, too weak, barely usable, old free model from 23 years ago.

Technical Status and Notes:

Some less common scenes show inconsistencies.

Use English for prompt words!

Older models are not good at generating realistic content. Try to use Cartoon style.

When using image prompts, some models will refuse to generate suggestive or large-scale content.

When 5 seconds and 10 seconds are optional, always use 5 seconds. Current models' 10-second videos are too empty.
