#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Instagram Ultimate Hunter V4 - Professional Edition with HTML Export
نسخة شاملة مع ميزة البحث عن اليوزرات النادرة وتصدير HTML احترافي
Developer: Kraar - Digital Creativity Company - Iraq
"""

import re
import json
import time
import random
import string
import requests
import os
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, asdict, field
from concurrent.futures import ThreadPoolExecutor, as_completed

# تكوين الألوان للطباعة
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

@dataclass
class AccountInfo:
    """معلومات الحساب الكاملة"""
    username: str
    user_id: Optional[str] = None
    full_name: Optional[str] = None
    biography: Optional[str] = None
    external_url: Optional[str] = None
    is_private: bool = False
    is_verified: bool = False
    profile_pic_url: Optional[str] = None
    
    # إحصائيات الحساب
    followers_count: int = 0
    following_count: int = 0
    posts_count: int = 0
    
    # معلومات التواصل والتسجيل
    email: Optional[str] = None
    phone_number: Optional[str] = None
    phone_country_code: Optional[str] = None
    public_email: Optional[str] = None
    public_phone_number: Optional[str] = None
    public_phone_country_code: Optional[str] = None
    
    # ربط الحسابات
    is_facebook_linked: bool = False
    facebook_id: Optional[str] = None
    facebook_name: Optional[str] = None
    facebook_profile_url: Optional[str] = None
    
    # معلومات الأعمال
    is_business_account: bool = False
    is_professional_account: bool = False
    business_category_name: Optional[str] = None
    category_name: Optional[str] = None
    business_contact_method: Optional[str] = None
    
    # معلومات المحتوى
    has_highlight_reels: bool = False
    highlight_reel_count: int = 0
    has_videos: bool = False
    has_saved_media: bool = False
    has_guides: bool = False
    
    # معلومات إضافية
    is_joined_recently: bool = False
    registration_date: Optional[str] = None
    last_post_date: Optional[str] = None
    account_type: str = "Personal"
    
    # بيانات المنشورات والستوري
    recent_posts: List[Dict] = field(default_factory=list)
    stories_count: int = 0
    has_active_stories: bool = False
    total_igtv_videos: int = 0
    total_reels: int = 0
    
    # معلومات التفاعل
    engagement_rate: float = 0.0
    average_likes: int = 0
    average_comments: int = 0
    
    # حالة التوفر
    availability_status: str = "taken"  # available, taken, unknown

@dataclass
class UsernameSearchResult:
    """نتيجة البحث عن يوزر"""
    username: str
    status: str  # available, taken, unknown
    account_info: Optional[AccountInfo] = None
    checked_at: str = field(default_factory=lambda: datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

class HTMLExporter:
    """فئة لتصدير النتائج بتنسيق HTML احترافي"""
    
    @staticmethod
    def get_html_template() -> str:
        """إنشاء قالب HTML احترافي"""
        return '''<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instagram Hunter Results - نتائج البحث</title>
    
    <!-- External Libraries -->
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Cairo:wght@300;400;600;700&display=swap" rel="stylesheet">
    <script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.0/dist/chart.umd.min.js"></script>
    
    <style>
        :root {
            --primary-color: #833AB4;
            --secondary-color: #C13584;
            --tertiary-color: #E1306C;
            --quaternary-color: #FD1D1D;
            --gradient: linear-gradient(135deg, #833AB4 0%, #FD1D1D 100%);
            --bg-color: #fafafa;
            --card-bg: #ffffff;
            --text-primary: #262626;
            --text-secondary: #8e8e8e;
            --border-color: #dbdbdb;
            --success-color: #00C853;
            --verified-color: #3897f0;
        }
        
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }
        
        body {
            font-family: 'Cairo', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif;
            background: var(--bg-color);
            color: var(--text-primary);
            line-height: 1.6;
            padding: 20px;
            min-height: 100vh;
        }
        
        /* Header */
        .header {
            background: var(--gradient);
            color: white;
            padding: 40px 20px;
            border-radius: 20px;
            text-align: center;
            margin-bottom: 40px;
            box-shadow: 0 10px 40px rgba(131, 58, 180, 0.3);
            animation: fadeInDown 0.6s ease;
        }
        
        .header h1 {
            font-size: 2.5em;
            font-weight: 700;
            margin-bottom: 10px;
            text-shadow: 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .header p {
            font-size: 1.1em;
            opacity: 0.95;
        }
        
        .header-btn {
            background: rgba(255,255,255,0.2);
            border: 2px solid white;
            color: white;
            padding: 10px 25px;
            border-radius: 25px;
            cursor: pointer;
            font-family: 'Cairo', sans-serif;
            font-weight: 600;
            transition: all 0.3s ease;
            font-size: 0.95em;
        }
        
        .header-btn:hover {
            background: white;
            color: var(--primary-color);
            transform: translateY(-2px);
            box-shadow: 0 4px 15px rgba(255,255,255,0.3);
        }
        
        /* Statistics Bar */
        .stats-bar {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 40px;
            animation: fadeInUp 0.6s ease 0.2s both;
        }
        
        .stat-card {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            text-align: center;
            transition: transform 0.3s ease, box-shadow 0.3s ease;
        }
        
        .stat-card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(0,0,0,0.12);
        }
        
        .stat-icon {
            font-size: 2.5em;
            margin-bottom: 15px;
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
        }
        
        .stat-value {
            font-size: 2em;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 5px;
        }
        
        .stat-label {
            color: var(--text-secondary);
            font-size: 0.95em;
        }
        
        /* Filters */
        .filters {
            background: var(--card-bg);
            padding: 25px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            animation: fadeIn 0.6s ease 0.4s both;
        }
        
        .filter-group {
            display: flex;
            gap: 15px;
            flex-wrap: wrap;
            align-items: center;
        }
        
        .filter-btn {
            padding: 12px 24px;
            border: 2px solid var(--border-color);
            background: white;
            border-radius: 25px;
            cursor: pointer;
            transition: all 0.3s ease;
            font-family: 'Cairo', sans-serif;
            font-size: 0.95em;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .filter-btn:hover {
            border-color: var(--primary-color);
            color: var(--primary-color);
            transform: translateY(-2px);
        }
        
        .filter-btn.active {
            background: var(--gradient);
            color: white;
            border-color: transparent;
        }
        
        .search-box {
            flex: 1;
            min-width: 300px;
            position: relative;
        }
        
        .search-box input {
            width: 100%;
            padding: 12px 45px 12px 20px;
            border: 2px solid var(--border-color);
            border-radius: 25px;
            font-family: 'Cairo', sans-serif;
            font-size: 0.95em;
            transition: all 0.3s ease;
        }
        
        .search-box input:focus {
            outline: none;
            border-color: var(--primary-color);
            box-shadow: 0 0 0 4px rgba(131, 58, 180, 0.1);
        }
        
        .search-box i {
            position: absolute;
            left: 20px;
            top: 50%;
            transform: translateY(-50%);
            color: var(--text-secondary);
        }
        
        /* Cards Grid */
        .accounts-grid {
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
            gap: 25px;
            margin-bottom: 40px;
        }
        
        .account-card {
            background: var(--card-bg);
            border-radius: 20px;
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
            cursor: pointer;
            transition: all 0.3s ease;
            animation: fadeInScale 0.5s ease;
        }
        
        .account-card:hover {
            transform: translateY(-8px);
            box-shadow: 0 12px 35px rgba(0,0,0,0.15);
        }
        
        .card-header {
            position: relative;
            padding: 30px 20px 20px;
            background: linear-gradient(135deg, rgba(131, 58, 180, 0.05) 0%, rgba(253, 29, 29, 0.05) 100%);
        }
        
        .profile-pic-wrapper {
            width: 100px;
            height: 100px;
            margin: 0 auto 15px;
            position: relative;
        }
        
        .profile-pic {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 4px solid white;
            object-fit: cover;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: block;
        }
        
        .profile-pic-placeholder {
            width: 100%;
            height: 100%;
            border-radius: 50%;
            border: 4px solid white;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2.5em;
            font-weight: 700;
            text-transform: uppercase;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        }
        
        /* Mobile image optimization */
        @media (max-width: 768px) {
            .profile-pic,
            .profile-pic-placeholder {
                border: 3px solid white;
            }
            
            .profile-pic-placeholder {
                font-size: 1.8em;
            }
        }
        
        .status-badge {
            position: absolute;
            top: 0;
            right: 0;
            width: 32px;
            height: 32px;
            border-radius: 50%;
            border: 3px solid white;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 0.9em;
            box-shadow: 0 2px 8px rgba(0,0,0,0.15);
        }
        
        .status-available {
            background: var(--success-color);
        }
        
        .status-taken {
            background: var(--tertiary-color);
        }
        
        .username-section {
            text-align: center;
            margin-bottom: 15px;
        }
        
        .username {
            font-size: 1.3em;
            font-weight: 700;
            color: var(--text-primary);
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 8px;
        }
        
        .verified-badge {
            color: var(--verified-color);
            font-size: 0.8em;
        }
        
        .full-name {
            color: var(--text-secondary);
            font-size: 0.95em;
        }
        
        .card-stats {
            display: flex;
            justify-content: space-around;
            padding: 20px;
            border-top: 1px solid var(--border-color);
            background: white;
        }
        
        .stat-item {
            text-align: center;
        }
        
        .stat-item-value {
            font-size: 1.2em;
            font-weight: 700;
            color: var(--text-primary);
            display: block;
        }
        
        .stat-item-label {
            font-size: 0.85em;
            color: var(--text-secondary);
            margin-top: 3px;
        }
        
        .card-footer {
            padding: 15px 20px;
            background: rgba(0,0,0,0.02);
            text-align: center;
        }
        
        .card-meta {
            padding: 15px 20px;
            background: rgba(131, 58, 180, 0.03);
            border-top: 1px solid var(--border-color);
        }
        
        .meta-item {
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 8px 0;
            font-size: 0.85em;
            color: var(--text-secondary);
        }
        
        .meta-item i {
            margin-left: 8px;
            color: var(--primary-color);
        }
        
        .meta-value {
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .view-details-btn {
            background: var(--gradient);
            color: white;
            border: none;
            padding: 10px 25px;
            border-radius: 20px;
            font-family: 'Cairo', sans-serif;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.9em;
        }
        
        .view-details-btn:hover {
            transform: scale(1.05);
            box-shadow: 0 4px 15px rgba(131, 58, 180, 0.4);
        }
        
        .action-buttons {
            display: flex;
            gap: 10px;
            justify-content: center;
            flex-wrap: wrap;
        }
        
        .action-btn {
            background: white;
            color: var(--primary-color);
            border: 2px solid var(--primary-color);
            padding: 8px 20px;
            border-radius: 20px;
            font-family: 'Cairo', sans-serif;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.3s ease;
            font-size: 0.85em;
            text-decoration: none;
            display: inline-flex;
            align-items: center;
            gap: 5px;
        }
        
        .action-btn:hover {
            background: var(--primary-color);
            color: white;
            transform: translateY(-2px);
        }
        
        .copy-notification {
            position: fixed;
            top: 20px;
            right: 20px;
            background: var(--success-color);
            color: white;
            padding: 15px 25px;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            z-index: 10000;
            animation: slideInRight 0.3s ease, slideOutRight 0.3s ease 2s;
            opacity: 0;
            pointer-events: none;
        }
        
        .copy-notification.show {
            opacity: 1;
            pointer-events: auto;
        }
        
        @keyframes slideInRight {
            from {
                transform: translateX(400px);
                opacity: 0;
            }
            to {
                transform: translateX(0);
                opacity: 1;
            }
        }
        
        @keyframes slideOutRight {
            from {
                transform: translateX(0);
                opacity: 1;
            }
            to {
                transform: translateX(400px);
                opacity: 0;
            }
        }
        
        .loading-spinner {
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(255,255,255,.3);
            border-radius: 50%;
            border-top-color: white;
            animation: spin 1s ease-in-out infinite;
        }
        
        @keyframes spin {
            to { transform: rotate(360deg); }
        }
        
        /* Loading Indicator */
        .page-loader {
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: var(--bg-color);
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            z-index: 9999;
            transition: opacity 0.3s ease;
        }
        
        .page-loader.hidden {
            opacity: 0;
            pointer-events: none;
        }
        
        .loader-spinner {
            width: 60px;
            height: 60px;
            border: 4px solid rgba(131, 58, 180, 0.1);
            border-top-color: var(--primary-color);
            border-radius: 50%;
            animation: spin 1s linear infinite;
        }
        
        .loader-text {
            margin-top: 20px;
            font-size: 1.2em;
            color: var(--primary-color);
            font-weight: 600;
        }
        
        /* Charts */
        .chart-container {
            position: relative;
            height: 400px;
            margin: 30px 0;
            background: white;
            padding: 20px;
            border-radius: 15px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        }
        
        .chart-title {
            text-align: center;
            font-size: 1.3em;
            font-weight: 700;
            color: var(--primary-color);
            margin-bottom: 20px;
        }
        
        /* Comparison */
        .comparison-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 20px;
            margin: 20px 0;
        }
        
        .comparison-card {
            background: linear-gradient(135deg, rgba(131, 58, 180, 0.05), rgba(253, 29, 29, 0.05));
            padding: 20px;
            border-radius: 15px;
            border: 2px solid var(--border-color);
            transition: all 0.3s ease;
        }
        
        .comparison-card:hover {
            border-color: var(--primary-color);
            transform: translateY(-5px);
            box-shadow: 0 8px 25px rgba(131, 58, 180, 0.15);
        }
        
        .comparison-card h4 {
            color: var(--primary-color);
            margin-bottom: 15px;
            font-size: 1.2em;
        }
        
        .vs-badge {
            background: var(--gradient);
            color: white;
            padding: 10px 20px;
            border-radius: 25px;
            font-weight: 700;
            display: inline-block;
            margin: 20px auto;
            text-align: center;
        }
        
        /* Modal */
        .modal {
            display: none;
            position: fixed;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0,0,0,0.8);
            z-index: 1000;
            animation: fadeIn 0.3s ease;
            overflow-y: auto;
            padding: 40px 20px;
        }
        
        .modal.active {
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .modal-content {
            background: var(--card-bg);
            border-radius: 25px;
            max-width: 800px;
            width: 100%;
            max-height: 90vh;
            overflow-y: auto;
            position: relative;
            animation: slideInUp 0.4s ease;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        }
        
        .modal-header {
            background: var(--gradient);
            color: white;
            padding: 30px;
            border-radius: 25px 25px 0 0;
            position: relative;
        }
        
        .close-modal {
            position: absolute;
            top: 20px;
            left: 20px;
            background: rgba(255,255,255,0.2);
            border: none;
            width: 40px;
            height: 40px;
            border-radius: 50%;
            cursor: pointer;
            color: white;
            font-size: 1.5em;
            transition: all 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .close-modal:hover {
            background: rgba(255,255,255,0.3);
            transform: rotate(90deg);
        }
        
        .modal-profile {
            display: flex;
            align-items: center;
            gap: 20px;
        }
        
        .modal-profile-pic {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 4px solid white;
            object-fit: cover;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        }
        
        .modal-profile-pic-placeholder {
            width: 100px;
            height: 100px;
            border-radius: 50%;
            border: 4px solid white;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-size: 2.5em;
            font-weight: 700;
        }
        
        .modal-profile-info h2 {
            font-size: 1.8em;
            margin-bottom: 5px;
        }
        
        .modal-body {
            padding: 30px;
        }
        
        .info-section {
            margin-bottom: 30px;
        }
        
        .info-section h3 {
            font-size: 1.3em;
            margin-bottom: 15px;
            color: var(--primary-color);
            display: flex;
            align-items: center;
            gap: 10px;
        }
        
        .info-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 15px;
        }
        
        .info-item {
            background: rgba(131, 58, 180, 0.05);
            padding: 15px;
            border-radius: 12px;
            border-right: 4px solid var(--primary-color);
        }
        
        .info-label {
            font-size: 0.85em;
            color: var(--text-secondary);
            margin-bottom: 5px;
        }
        
        .info-value {
            font-size: 1.1em;
            font-weight: 600;
            color: var(--text-primary);
        }
        
        .biography {
            background: rgba(131, 58, 180, 0.05);
            padding: 20px;
            border-radius: 12px;
            line-height: 1.8;
            color: var(--text-primary);
        }
        
        .tag {
            display: inline-block;
            padding: 6px 15px;
            background: var(--gradient);
            color: white;
            border-radius: 20px;
            font-size: 0.85em;
            margin: 5px;
            font-weight: 600;
        }
        
        /* Animations */
        @keyframes fadeIn {
            from {
                opacity: 0;
            }
            to {
                opacity: 1;
            }
        }
        
        @keyframes fadeInDown {
            from {
                opacity: 0;
                transform: translateY(-30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInUp {
            from {
                opacity: 0;
                transform: translateY(30px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
        
        @keyframes fadeInScale {
            from {
                opacity: 0;
                transform: scale(0.9);
            }
            to {
                opacity: 1;
                transform: scale(1);
            }
        }
        
        @keyframes slideInUp {
            from {
                transform: translateY(50px);
                opacity: 0;
            }
            to {
                transform: translateY(0);
                opacity: 1;
            }
        }
        
        /* Responsive Design - Mobile First */
        /* Mobile Phones */
        @media (max-width: 768px) {
            .container {
                padding: 0;
            }
            
            .header {
                padding: 25px 15px;
            }
            
            .header h1 {
                font-size: 1.5em;
            }
            
            .header p {
                font-size: 0.85em;
            }
            
            .header > div {
                flex-direction: column;
                gap: 8px;
                margin-top: 15px;
            }
            
            .header-btn {
                width: 100%;
                padding: 10px 18px;
                font-size: 0.85em;
            }
            
            .stats {
                grid-template-columns: repeat(2, 1fr);
                gap: 10px;
                padding: 15px;
                margin: 15px;
            }
            
            .stat-card {
                padding: 15px 10px;
            }
            
            .stat-icon {
                font-size: 1.5em;
            }
            
            .stat-value {
                font-size: 1.3em;
            }
            
            .stat-label {
                font-size: 0.7em;
            }
            
            .filters {
                padding: 15px;
                flex-direction: column;
                gap: 12px;
            }
            
            .filter-buttons {
                flex-wrap: wrap;
                justify-content: center;
                gap: 6px;
            }
            
            .filter-btn {
                font-size: 0.75em;
                padding: 7px 12px;
                flex: 0 0 auto;
            }
            
            #searchInput {
                width: 100%;
                font-size: 0.9em;
                padding: 10px 35px 10px 12px;
            }
            
            .accounts-grid {
                grid-template-columns: 1fr;
                gap: 15px;
                padding: 15px;
            }
            
            .account-card {
                max-width: 100%;
            }
            
            .card-header {
                padding: 15px;
            }
            
            .profile-pic-wrapper {
                width: 70px;
                height: 70px;
            }
            
            .username {
                font-size: 0.95em;
            }
            
            .full-name {
                font-size: 0.8em;
            }
            
            .card-stats {
                grid-template-columns: repeat(3, 1fr);
                padding: 12px;
                gap: 8px;
            }
            
            .stat-item-value {
                font-size: 1.1em;
            }
            
            .stat-item-label {
                font-size: 0.7em;
            }
            
            .card-meta {
                padding: 12px 15px;
            }
            
            .meta-item {
                font-size: 0.8em;
                padding: 6px 0;
            }
            
            .card-footer {
                padding: 12px 15px;
            }
            
            .action-buttons {
                flex-direction: column;
                width: 100%;
                gap: 8px;
            }
            
            .action-btn,
            .view-details-btn {
                width: 100%;
                font-size: 0.85em;
                padding: 10px 20px;
            }
            
            .modal-content {
                width: 95%;
                max-width: 95%;
                margin: 15px auto;
                max-height: 90vh;
                padding: 15px;
            }
            
            .modal-header {
                padding: 15px;
            }
            
            .modal-profile-pic,
            .modal-profile-pic-placeholder {
                width: 70px;
                height: 70px;
            }
            
            .modal-username {
                font-size: 1.1em;
            }
            
            .modal-full-name {
                font-size: 0.85em;
            }
            
            .close-modal {
                top: 10px;
                left: 10px;
                width: 35px;
                height: 35px;
                font-size: 1.3em;
            }
            
            .modal-body {
                padding: 15px;
            }
            
            .info-section {
                margin-bottom: 20px;
            }
            
            .info-section h3 {
                font-size: 1.1em;
                margin-bottom: 12px;
            }
            
            .info-grid {
                grid-template-columns: 1fr;
                gap: 10px;
            }
            
            .info-item {
                padding: 10px;
            }
            
            .info-label {
                font-size: 0.8em;
            }
            
            .info-value {
                font-size: 0.85em;
            }
            
            .chart-container {
                height: 300px;
                padding: 15px;
            }
            
            .comparison-grid {
                grid-template-columns: 1fr;
            }
            
            .comparison-card {
                padding: 15px;
            }
            
            .vs-badge {
                margin: 15px 0;
                padding: 8px 16px;
                font-size: 0.9em;
            }
            
            .empty-state {
                padding: 50px 20px;
            }
            
            .empty-state i {
                font-size: 3em;
            }
            
            .empty-state h3 {
                font-size: 1.2em;
            }
            
            .empty-state p {
                font-size: 0.9em;
            }
        }
        
        /* Small Mobile Phones */
        @media (max-width: 480px) {
            .header h1 {
                font-size: 1.3em;
            }
            
            .header p {
                font-size: 0.8em;
            }
            
            .stats {
                grid-template-columns: 1fr;
                gap: 8px;
            }
            
            .profile-pic-wrapper {
                width: 60px;
                height: 60px;
            }
            
            .username {
                font-size: 0.9em;
            }
            
            .full-name {
                font-size: 0.75em;
            }
            
            .stat-item-value {
                font-size: 1em;
            }
            
            .stat-item-label {
                font-size: 0.65em;
            }
            
            .filter-btn {
                font-size: 0.7em;
                padding: 6px 10px;
            }
            
            .header-btn {
                font-size: 0.8em;
                padding: 9px 15px;
            }
        }
        
        /* Tablet */
        @media (min-width: 769px) and (max-width: 1024px) {
            .accounts-grid {
                grid-template-columns: repeat(2, 1fr);
                gap: 20px;
                padding: 20px;
            }
            
            .modal-content {
                width: 85%;
                max-width: 700px;
            }
            
            .stats {
                padding: 20px;
            }
        }
        
        /* Desktop */
        @media (min-width: 1025px) {
            .accounts-grid {
                grid-template-columns: repeat(3, 1fr);
            }
        }
        
        /* Large Desktop */
        @media (min-width: 1441px) {
            .container {
                max-width: 1600px;
            }
            
            .accounts-grid {
                grid-template-columns: repeat(4, 1fr);
            }
        }
        
        /* Landscape Mobile */
        @media (max-width: 896px) and (orientation: landscape) {
            .header {
                padding: 20px 15px;
            }
            
            .header h1 {
                font-size: 1.4em;
            }
            
            .stats {
                grid-template-columns: repeat(4, 1fr);
            }
            
            .accounts-grid {
                grid-template-columns: repeat(2, 1fr);
            }
            
            .modal-content {
                max-height: 85vh;
            }
        }
        
        /* Empty State */
        .empty-state {
            text-align: center;
            padding: 80px 20px;
            color: var(--text-secondary);
        }
        
        .empty-state i {
            font-size: 5em;
            margin-bottom: 20px;
            opacity: 0.3;
        }
        
        .empty-state h3 {
            font-size: 1.5em;
            margin-bottom: 10px;
        }
        
        /* Footer */
        .footer {
            text-align: center;
            padding: 40px 20px;
            color: var(--text-secondary);
            margin-top: 60px;
        }
        
        .footer .brand {
            background: var(--gradient);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            background-clip: text;
            font-weight: 700;
            font-size: 1.2em;
            margin-top: 10px;
        }
        
        /* Print Styles */
        @media print {
            body {
                background: white;
            }
            
            .filters,
            .view-details-btn,
            .action-btn,
            .footer,
            .header > div {
                display: none !important;
            }
            
            .account-card {
                break-inside: avoid;
                page-break-inside: avoid;
            }
            
            .modal {
                display: none !important;
            }
        }
    </style>
</head>
<body>
    <!-- Page Loader -->
    <div class="page-loader" id="pageLoader">
        <div class="loader-spinner"></div>
        <div class="loader-text">جاري تحميل البيانات...</div>
    </div>
    
    <!-- Header -->
    <div class="header">
        <h1><i class="fab fa-instagram"></i> Instagram Hunter Results</h1>
        <p>نتائج البحث الاحترافية - شركة الإبداع الرقمي</p>
        <div style="margin-top: 20px; display: flex; gap: 15px; justify-content: center; flex-wrap: wrap;">
            <button onclick="exportToJSON()" class="header-btn">
                <i class="fas fa-download"></i> JSON
            </button>
            <button onclick="exportToCSV()" class="header-btn">
                <i class="fas fa-file-csv"></i> CSV
            </button>
            <button onclick="printResults()" class="header-btn">
                <i class="fas fa-print"></i> طباعة
            </button>
            <button onclick="showStatisticsModal()" class="header-btn">
                <i class="fas fa-chart-pie"></i> إحصائيات
            </button>
            <button onclick="showChartsModal()" class="header-btn">
                <i class="fas fa-chart-line"></i> رسوم بيانية
            </button>
            <button onclick="compareAccounts()" class="header-btn">
                <i class="fas fa-balance-scale"></i> مقارنة
            </button>
        </div>
    </div>
    
    <!-- Statistics -->
    <div class="stats-bar">
        <div class="stat-card">
            <div class="stat-icon"><i class="fas fa-users"></i></div>
            <div class="stat-value" id="totalAccounts">0</div>
            <div class="stat-label">إجمالي الحسابات</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"><i class="fas fa-check-circle"></i></div>
            <div class="stat-value" id="availableCount">0</div>
            <div class="stat-label">متاح</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"><i class="fas fa-user-check"></i></div>
            <div class="stat-value" id="takenCount">0</div>
            <div class="stat-label">محجوز</div>
        </div>
        <div class="stat-card">
            <div class="stat-icon"><i class="fas fa-calendar"></i></div>
            <div class="stat-value" id="searchDate">-</div>
            <div class="stat-label">تاريخ البحث</div>
        </div>
    </div>
    
    <!-- Filters -->
    <div class="filters">
        <div class="filter-group">
            <button class="filter-btn active" onclick="filterAccounts('all')">
                <i class="fas fa-th"></i> الكل
            </button>
            <button class="filter-btn" onclick="filterAccounts('available')">
                <i class="fas fa-check-circle"></i> متاح
            </button>
            <button class="filter-btn" onclick="filterAccounts('taken')">
                <i class="fas fa-user"></i> محجوز
            </button>
            <button class="filter-btn" onclick="filterAccounts('verified')">
                <i class="fas fa-check-circle"></i> موثق
            </button>
            <button class="filter-btn" onclick="filterAccounts('business')">
                <i class="fas fa-briefcase"></i> أعمال
            </button>
            <div class="search-box">
                <input type="text" id="searchInput" placeholder="ابحث عن اسم مستخدم..." onkeyup="searchAccounts()">
                <i class="fas fa-search"></i>
            </div>
        </div>
    </div>
    
    <!-- Accounts Grid -->
    <div class="accounts-grid" id="accountsGrid">
        <!-- Cards will be inserted here by JavaScript -->
    </div>
    
    <!-- Empty State -->
    <div class="empty-state" id="emptyState" style="display: none;">
        <i class="fas fa-search"></i>
        <h3>لا توجد نتائج</h3>
        <p>لم يتم العثور على حسابات تطابق البحث</p>
    </div>
    
    <!-- Modal -->
    <div class="modal" id="accountModal">
        <div class="modal-content">
            <div class="modal-header">
                <button class="close-modal" onclick="closeModal()">
                    <i class="fas fa-times"></i>
                </button>
                <div class="modal-profile">
                    <div id="modalProfilePicContainer">
                        <img src="" alt="Profile" class="modal-profile-pic" id="modalProfilePic">
                    </div>
                    <div class="modal-profile-info">
                        <h2 id="modalUsername"></h2>
                        <p id="modalFullName"></p>
                    </div>
                </div>
            </div>
            <div class="modal-body" id="modalBody">
                <!-- Details will be inserted here by JavaScript -->
            </div>
        </div>
    </div>
    
    <!-- Footer -->
    <div class="footer">
        <p>تم الإنشاء باستخدام Instagram Ultimate Hunter V4</p>
        <p class="brand">Kraar - Digital Creativity Company - Iraq 🇮🇶</p>
    </div>
    
    <script>
        // Load data from JSON file
        let accountsData = [];
        
        // Initialize
        document.addEventListener('DOMContentLoaded', function() {
            console.log('🚀 بدء تهيئة الصفحة...');
            loadDataFromJSON();
        });
        
        // Load data from JSON file
        async function loadDataFromJSON() {
            try {
                console.log('📥 جاري تحميل البيانات من ملف JSON...');
                
                // Try to load from data.json
                const response = await fetch('data.json');
                
                if (!response.ok) {
                    throw new Error('لم يتم العثور على ملف البيانات');
                }
                
                accountsData = await response.json();
                console.log('✅ تم تحميل البيانات بنجاح:', accountsData.length, 'حساب');
                
                // Initialize UI
                updateStatistics();
                renderAccounts(accountsData);
                console.log('✅ تم تهيئة الصفحة بنجاح');
                
                // Hide loader
                hideLoader();
                
            } catch (error) {
                console.error('❌ خطأ في تحميل البيانات:', error);
                
                // Show error to user
                if (error.message.includes('لم يتم العثور')) {
                    showError(`
                        <div style="text-align: center;">
                            <i class="fas fa-folder-open" style="font-size: 4em; color: var(--text-secondary); margin-bottom: 20px;"></i>
                            <h3>لا توجد بيانات للعرض</h3>
                            <p>لم يتم العثور على ملف البيانات (data.json)</p>
                            <p style="color: var(--text-secondary); font-size: 0.9em; margin-top: 15px;">
                                قم بالبحث عن حسابات أولاً من البرنامج الرئيسي
                            </p>
                        </div>
                    `);
                } else {
                    showError(`
                        <div style="text-align: center;">
                            <i class="fas fa-exclamation-triangle" style="font-size: 4em; color: var(--quaternary-color); margin-bottom: 20px;"></i>
                            <h3>حدث خطأ في تحميل البيانات</h3>
                            <p>${error.message}</p>
                            <p style="color: var(--text-secondary); font-size: 0.9em; margin-top: 15px;">
                                افتح Developer Console (F12) لمزيد من التفاصيل
                            </p>
                        </div>
                    `);
                }
                
                hideLoader();
            }
        }
        
        // Hide loader
        function hideLoader() {
            setTimeout(() => {
                const loader = document.getElementById('pageLoader');
                if (loader) {
                    loader.classList.add('hidden');
                    setTimeout(() => loader.remove(), 300);
                }
            }, 300);
        }
        
        // Update Statistics
        function updateStatistics() {
            try {
                const total = accountsData.length;
                const available = accountsData.filter(acc => acc.status === 'available').length;
                const taken = accountsData.filter(acc => acc.status === 'taken').length;
                
                document.getElementById('totalAccounts').textContent = total;
                document.getElementById('availableCount').textContent = available;
                document.getElementById('takenCount').textContent = taken;
                
                if (accountsData.length > 0 && accountsData[0].checked_at) {
                    const date = new Date(accountsData[0].checked_at);
                    document.getElementById('searchDate').textContent = date.toLocaleDateString('ar-IQ');
                }
                
                console.log('✅ تم تحديث الإحصائيات:', {total, available, taken});
            } catch (error) {
                console.error('❌ خطأ في تحديث الإحصائيات:', error);
            }
        }
        
        // Show error message
        function showError(htmlContent) {
            const grid = document.getElementById('accountsGrid');
            const emptyState = document.getElementById('emptyState');
            
            if (grid) grid.style.display = 'none';
            if (emptyState) {
                emptyState.style.display = 'block';
                emptyState.innerHTML = htmlContent;
            }
        }
        
        // Render Accounts
        function renderAccounts(accounts) {
            const grid = document.getElementById('accountsGrid');
            const emptyState = document.getElementById('emptyState');
            
            try {
                console.log('🎨 بدء عرض الحسابات:', accounts.length);
                
                if (!accounts || accounts.length === 0) {
                    grid.style.display = 'none';
                    emptyState.style.display = 'block';
                    console.log('⚠️ لا توجد حسابات للعرض');
                    return;
                }
                
                grid.style.display = 'grid';
                emptyState.style.display = 'none';
                grid.innerHTML = '';
                
                accounts.forEach((account, index) => {
                    try {
                        const card = createAccountCard(account, index);
                        grid.appendChild(card);
                    } catch (error) {
                        console.error('❌ خطأ في إنشاء بطاقة:', account.username, error);
                    }
                });
                
                console.log('✅ تم عرض', accounts.length, 'حساب بنجاح');
            } catch (error) {
                console.error('❌ خطأ في عرض الحسابات:', error);
                showError('حدث خطأ في عرض الحسابات');
            }
        }
        
        // Create Account Card
        function createAccountCard(account, index) {
            try {
                const div = document.createElement('div');
                div.className = 'account-card';
                div.dataset.status = account.status || 'unknown';
                div.dataset.verified = account.account_info?.is_verified || false;
                div.dataset.business = account.account_info?.is_business_account || false;
                div.dataset.username = (account.username || '').toLowerCase();
                
                const accountInfo = account.account_info || {};
                const hasProfilePic = accountInfo.profile_pic_url && accountInfo.profile_pic_url !== '';
                const firstLetter = (account.username || 'U')[0].toUpperCase();
                const fullName = accountInfo.full_name || account.username || 'مستخدم';
                const followers = formatNumber(accountInfo.followers_count || 0);
                const following = formatNumber(accountInfo.following_count || 0);
                const posts = formatNumber(accountInfo.posts_count || 0);
                const isVerified = accountInfo.is_verified || false;
                const statusClass = account.status === 'available' ? 'status-available' : 'status-taken';
                const statusIcon = account.status === 'available' ? '✓' : '●';
                
                // Format dates safely
                let joinDate = '-';
                let lastActivity = '-';
                let checkedDate = '-';
                
                try {
                    if (accountInfo.registration_date) {
                        joinDate = accountInfo.registration_date;
                    } else if (accountInfo.is_joined_recently) {
                        joinDate = 'منضم حديثاً';
                    }
                    
                    if (accountInfo.last_post_date) {
                        lastActivity = accountInfo.last_post_date;
                    }
                    
                    if (account.checked_at) {
                        const date = new Date(account.checked_at);
                        checkedDate = date.toLocaleDateString('ar-IQ', {
                            year: 'numeric',
                            month: 'short',
                            day: 'numeric'
                        });
                    }
                } catch (dateError) {
                    console.warn('⚠️ خطأ في معالجة التواريخ:', dateError);
                }
                
                div.innerHTML = `
                    <div class="card-header">
                        <div class="profile-pic-wrapper">
                            ${hasProfilePic ? 
                                `<img src="${accountInfo.profile_pic_url}" alt="${account.username}" class="profile-pic" 
                                    onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                                <div class="profile-pic-placeholder" style="display:none;">${firstLetter}</div>` :
                                `<div class="profile-pic-placeholder">${firstLetter}</div>`
                            }
                            <div class="status-badge ${statusClass}">${statusIcon}</div>
                        </div>
                        <div class="username-section">
                            <div class="username">
                                @${account.username}
                                ${isVerified ? '<i class="fas fa-check-circle verified-badge"></i>' : ''}
                            </div>
                            <div class="full-name">${fullName}</div>
                        </div>
                    </div>
                    
                    ${account.status === 'taken' ? `
                        <div class="card-stats">
                            <div class="stat-item">
                                <span class="stat-item-value">${posts}</span>
                                <span class="stat-item-label">منشور</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-item-value">${followers}</span>
                                <span class="stat-item-label">متابع</span>
                            </div>
                            <div class="stat-item">
                                <span class="stat-item-value">${following}</span>
                                <span class="stat-item-label">متابَع</span>
                            </div>
                        </div>
                        
                        <div class="card-meta">
                            ${joinDate !== '-' ? `
                                <div class="meta-item">
                                    <span><i class="fas fa-calendar-plus"></i> تاريخ الانضمام</span>
                                    <span class="meta-value">${joinDate}</span>
                                </div>
                            ` : ''}
                            ${lastActivity !== '-' ? `
                                <div class="meta-item">
                                    <span><i class="fas fa-clock"></i> آخر نشاط</span>
                                    <span class="meta-value">${lastActivity}</span>
                                </div>
                            ` : ''}
                            <div class="meta-item">
                                <span><i class="fas fa-search"></i> تاريخ الفحص</span>
                                <span class="meta-value">${checkedDate}</span>
                            </div>
                        </div>
                        
                        <div class="card-footer">
                            <div class="action-buttons">
                                <button class="view-details-btn" data-account-index="${index}" onclick="showAccountDetailsByIndex(${index})"> 
                                    <i class="fas fa-eye"></i> عرض التفاصيل
                                </button>
                                <button class="action-btn" onclick="copyUsername('${account.username}')">
                                    <i class="fas fa-copy"></i> نسخ
                                </button>
                                <a href="https://instagram.com/${account.username}" target="_blank" class="action-btn">
                                    <i class="fab fa-instagram"></i> فتح
                                </a>
                            </div>
                        </div>
                    ` : `
                        <div class="card-meta">
                            <div class="meta-item">
                                <span><i class="fas fa-search"></i> تاريخ الفحص</span>
                                <span class="meta-value">${checkedDate}</span>
                            </div>
                        </div>
                        <div class="card-footer">
                            <div style="padding: 15px; background: linear-gradient(135deg, rgba(0, 200, 83, 0.1), rgba(0, 200, 83, 0.2)); border-radius: 10px; margin: 10px;">
                                <div style="color: var(--success-color); font-weight: 700; font-size: 1.1em; margin-bottom: 8px;">
                                    <i class="fas fa-check-circle"></i> هذا الاسم متاح للحجز!
                                </div>
                                <div style="color: var(--text-secondary); font-size: 0.9em;">
                                    يمكنك استخدام هذا الاسم لإنشاء حساب جديد
                                </div>
                            </div>
                            <div class="action-buttons">
                                <button class="action-btn" onclick="copyUsername('${account.username}')">
                                    <i class="fas fa-copy"></i> نسخ الاسم
                                </button>
                                <a href="https://www.instagram.com/accounts/emailsignup/?username=${account.username}" target="_blank" class="action-btn" style="background: var(--success-color); color: white; border-color: var(--success-color);">
                                    <i class="fas fa-user-plus"></i> إنشاء حساب
                                </a>
                            </div>
                        </div>
                    `}
                `;
                
                return div;
            } catch (error) {
                console.error('❌ خطأ في createAccountCard:', error);
                // Create error card
                const errorDiv = document.createElement('div');
                errorDiv.className = 'account-card';
                errorDiv.innerHTML = `
                    <div style="padding: 20px; text-align: center; color: var(--quaternary-color);">
                        <i class="fas fa-exclamation-triangle"></i>
                        <p>خطأ في عرض البطاقة</p>
                    </div>
                `;
                return errorDiv;
            }
        }
        
        // Show Account Details by Index
        function showAccountDetailsByIndex(index) {
            const account = accountsData[index];
            if (account) {
                showAccountDetails(account);
            }
        }
        
        // Show Account Details in Modal
        function showAccountDetails(account) {
            const modal = document.getElementById('accountModal');
            const modalBody = document.getElementById('modalBody');
            const accountInfo = account.account_info || {};
            
            const hasProfilePic = accountInfo.profile_pic_url && accountInfo.profile_pic_url !== '';
            const firstLetter = account.username[0].toUpperCase();
            
            // Update header with better image handling
            const modalProfilePicContainer = document.getElementById('modalProfilePic').parentElement;
            if (hasProfilePic) {
                modalProfilePicContainer.innerHTML = `
                    <img src="${accountInfo.profile_pic_url}" alt="Profile" class="modal-profile-pic" id="modalProfilePic"
                        onerror="this.style.display='none'; this.nextElementSibling.style.display='flex';">
                    <div class="modal-profile-pic-placeholder" style="display:none;">${firstLetter}</div>
                `;
            } else {
                modalProfilePicContainer.innerHTML = `
                    <div class="modal-profile-pic-placeholder">${firstLetter}</div>
                `;
            }
            
            document.getElementById('modalUsername').innerHTML = `@${account.username} ${accountInfo.is_verified ? '<i class="fas fa-check-circle verified-badge"></i>' : ''}`;
            document.getElementById('modalFullName').textContent = accountInfo.full_name || '';
            
            // Build detailed info
            let detailsHTML = '';
            
            // Biography
            if (accountInfo.biography) {
                detailsHTML += `
                    <div class="info-section">
                        <h3><i class="fas fa-info-circle"></i> السيرة الذاتية</h3>
                        <div class="biography">${escapeHtml(accountInfo.biography)}</div>
                    </div>
                `;
            }
            
            // Basic Info
            detailsHTML += `
                <div class="info-section">
                    <h3><i class="fas fa-user"></i> المعلومات الأساسية</h3>
                    <div class="info-grid">
                        ${createInfoItem('نوع الحساب', accountInfo.account_type || 'شخصي')}
                        ${accountInfo.category_name ? createInfoItem('الفئة', accountInfo.category_name) : ''}
                        ${createInfoItem('حالة الخصوصية', accountInfo.is_private ? 'خاص 🔒' : 'عام 🌐')}
                        ${createInfoItem('الحالة', accountInfo.is_verified ? 'موثق ✓' : 'غير موثق')}
                    </div>
                </div>
            `;
            
            // Timeline Info
            if (accountInfo.is_joined_recently || accountInfo.registration_date || accountInfo.last_post_date || account.checked_at) {
                detailsHTML += `
                    <div class="info-section">
                        <h3><i class="fas fa-history"></i> الجدول الزمني</h3>
                        <div class="info-grid">
                            ${accountInfo.is_joined_recently ? createInfoItem('الانضمام', 'منضم حديثاً 🆕') : ''}
                            ${accountInfo.registration_date ? createInfoItem('تاريخ التسجيل', accountInfo.registration_date) : ''}
                            ${accountInfo.last_post_date ? createInfoItem('آخر منشور', accountInfo.last_post_date) : ''}
                            ${account.checked_at ? createInfoItem('تاريخ الفحص', new Date(account.checked_at).toLocaleString('ar-IQ')) : ''}
                        </div>
                    </div>
                `;
            }
            
            // Statistics
            detailsHTML += `
                <div class="info-section">
                    <h3><i class="fas fa-chart-line"></i> الإحصائيات التفصيلية</h3>
                    <div class="info-grid">
                        ${createInfoItem('المتابعون', formatNumber(accountInfo.followers_count || 0) + ' 👥')}
                        ${createInfoItem('المتابَعون', formatNumber(accountInfo.following_count || 0) + ' 👤')}
                        ${createInfoItem('المنشورات', formatNumber(accountInfo.posts_count || 0) + ' 📸')}
                        ${accountInfo.engagement_rate ? createInfoItem('معدل التفاعل', accountInfo.engagement_rate.toFixed(2) + '% 📊') : ''}
                        ${accountInfo.average_likes ? createInfoItem('متوسط الإعجابات', formatNumber(accountInfo.average_likes) + ' ❤️') : ''}
                        ${accountInfo.average_comments ? createInfoItem('متوسط التعليقات', formatNumber(accountInfo.average_comments) + ' 💬') : ''}
                    </div>
                </div>
            `;
            
            // Content Info
            if (accountInfo.has_highlight_reels || accountInfo.total_reels || accountInfo.total_igtv_videos || accountInfo.stories_count) {
                detailsHTML += `
                    <div class="info-section">
                        <h3><i class="fas fa-video"></i> المحتوى</h3>
                        <div class="info-grid">
                            ${accountInfo.has_highlight_reels ? createInfoItem('القصص المميزة', accountInfo.highlight_reel_count + ' 🎬') : ''}
                            ${accountInfo.total_reels ? createInfoItem('Reels', accountInfo.total_reels + ' 🎥') : ''}
                            ${accountInfo.total_igtv_videos ? createInfoItem('IGTV', accountInfo.total_igtv_videos + ' 📺') : ''}
                            ${accountInfo.stories_count ? createInfoItem('Stories', accountInfo.stories_count + ' 📱') : ''}
                        </div>
                    </div>
                `;
            }
            
            // Contact Info
            if (accountInfo.public_email || accountInfo.public_phone_number || accountInfo.external_url) {
                detailsHTML += `
                    <div class="info-section">
                        <h3><i class="fas fa-envelope"></i> معلومات التواصل</h3>
                        <div class="info-grid">
                            ${accountInfo.public_email ? createInfoItem('البريد الإلكتروني', `<a href="mailto:${accountInfo.public_email}" target="_blank">${accountInfo.public_email}</a> 📧`) : ''}
                            ${accountInfo.public_phone_number ? createInfoItem('رقم الهاتف', accountInfo.public_phone_number + ' 📱') : ''}
                            ${accountInfo.external_url ? createInfoItem('الموقع', `<a href="${accountInfo.external_url}" target="_blank">${accountInfo.external_url}</a> 🔗`) : ''}
                        </div>
                    </div>
                `;
            }
            
            // Business Info
            if (accountInfo.is_business_account || accountInfo.is_professional_account) {
                detailsHTML += `
                    <div class="info-section">
                        <h3><i class="fas fa-briefcase"></i> معلومات الأعمال</h3>
                        <div class="info-grid">
                            ${createInfoItem('حساب أعمال', accountInfo.is_business_account ? 'نعم ✓' : 'لا ✗')}
                            ${createInfoItem('حساب احترافي', accountInfo.is_professional_account ? 'نعم ✓' : 'لا ✗')}
                            ${accountInfo.business_category_name ? createInfoItem('فئة الأعمال', accountInfo.business_category_name + ' 💼') : ''}
                            ${accountInfo.business_contact_method ? createInfoItem('طريقة التواصل', accountInfo.business_contact_method + ' 📞') : ''}
                        </div>
                    </div>
                `;
            }
            
            // Facebook Connection
            if (accountInfo.is_facebook_linked) {
                detailsHTML += `
                    <div class="info-section">
                        <h3><i class="fab fa-facebook"></i> ربط Facebook</h3>
                        <div class="info-grid">
                            ${accountInfo.facebook_name ? createInfoItem('اسم Facebook', accountInfo.facebook_name) : ''}
                            ${accountInfo.facebook_id ? createInfoItem('معرف Facebook', accountInfo.facebook_id) : ''}
                            ${accountInfo.facebook_profile_url ? createInfoItem('رابط Facebook', `<a href="${accountInfo.facebook_profile_url}" target="_blank">زيارة الملف الشخصي</a>`) : ''}
                        </div>
                    </div>
                `;
            }
            
            // Tags
            let tags = [];
            if (accountInfo.is_verified) tags.push('موثق ✓');
            if (accountInfo.is_business_account) tags.push('أعمال 💼');
            if (accountInfo.is_professional_account) tags.push('احترافي 🎯');
            if (accountInfo.is_private) tags.push('خاص 🔒');
            if (accountInfo.has_highlight_reels) tags.push('قصص مميزة 🎬');
            if (accountInfo.is_joined_recently) tags.push('منضم حديثاً 🆕');
            if (account.status === 'available') tags.push('متاح 🟢');
            
            if (tags.length > 0) {
                detailsHTML += `
                    <div class="info-section">
                        <h3><i class="fas fa-tags"></i> الوسوم</h3>
                        <div>
                            ${tags.map(tag => `<span class="tag">${tag}</span>`).join('')}
                        </div>
                    </div>
                `;
            }
            
            modalBody.innerHTML = detailsHTML;
            modal.classList.add('active');
        }
        
        // Escape HTML to prevent XSS
        function escapeHtml(text) {
            const div = document.createElement('div');
            div.textContent = text;
            return div.innerHTML;
        }
        
        // Create Info Item
        function createInfoItem(label, value) {
            return `
                <div class="info-item">
                    <div class="info-label">${label}</div>
                    <div class="info-value">${value}</div>
                </div>
            `;
        }
        
        // Close Modal
        function closeModal() {
            document.getElementById('accountModal').classList.remove('active');
        }
        
        // Filter Accounts
        function filterAccounts(filter) {
            // Update active button
            const allButtons = document.querySelectorAll('.filter-btn');
            allButtons.forEach(btn => {
                btn.classList.remove('active');
            });
            event.target.classList.add('active');
            
            // Clear search box
            document.getElementById('searchInput').value = '';
            
            // Filter cards
            let filteredAccounts = [...accountsData];
            
            if (filter === 'available') {
                filteredAccounts = accountsData.filter(acc => acc.status === 'available');
            } else if (filter === 'taken') {
                filteredAccounts = accountsData.filter(acc => acc.status === 'taken');
            } else if (filter === 'verified') {
                filteredAccounts = accountsData.filter(acc => acc.account_info && acc.account_info.is_verified === true);
            } else if (filter === 'business') {
                filteredAccounts = accountsData.filter(acc => acc.account_info && acc.account_info.is_business_account === true);
            }
            
            console.log('Filter:', filter, 'Results:', filteredAccounts.length);
            renderAccounts(filteredAccounts);
        }
        
        // Search Accounts
        function searchAccounts() {
            const searchTerm = document.getElementById('searchInput').value.toLowerCase();
            
            if (searchTerm === '') {
                renderAccounts(accountsData);
                return;
            }
            
            const filtered = accountsData.filter(acc => {
                const username = acc.username.toLowerCase();
                const fullName = (acc.account_info?.full_name || '').toLowerCase();
                const biography = (acc.account_info?.biography || '').toLowerCase();
                
                return username.includes(searchTerm) || 
                       fullName.includes(searchTerm) || 
                       biography.includes(searchTerm);
            });
            
            renderAccounts(filtered);
        }
        
        // Format Number
        function formatNumber(num) {
            if (num >= 1000000) {
                return (num / 1000000).toFixed(1) + 'M';
            } else if (num >= 1000) {
                return (num / 1000).toFixed(1) + 'K';
            }
            return num.toString();
        }
        
        // Close modal on outside click
        document.getElementById('accountModal').addEventListener('click', function(e) {
            if (e.target === this) {
                closeModal();
            }
        });
        
        // Close modal on ESC key
        document.addEventListener('keydown', function(e) {
            if (e.key === 'Escape') {
                closeModal();
            }
        });
        
        // Copy username to clipboard
        function copyUsername(username) {
            const textArea = document.createElement('textarea');
            textArea.value = '@' + username;
            textArea.style.position = 'fixed';
            textArea.style.left = '-999999px';
            document.body.appendChild(textArea);
            textArea.select();
            
            try {
                document.execCommand('copy');
                showCopyNotification('تم نسخ @' + username);
            } catch (err) {
                console.error('Failed to copy:', err);
            }
            
            document.body.removeChild(textArea);
        }
        
        // Show copy notification
        function showCopyNotification(message) {
            // Remove any existing notification
            const existingNotification = document.querySelector('.copy-notification');
            if (existingNotification) {
                existingNotification.remove();
            }
            
            // Create new notification
            const notification = document.createElement('div');
            notification.className = 'copy-notification show';
            notification.innerHTML = `<i class="fas fa-check-circle"></i> ${message}`;
            document.body.appendChild(notification);
            
            // Remove after 2.5 seconds
            setTimeout(() => {
                notification.classList.remove('show');
                setTimeout(() => notification.remove(), 300);
            }, 2500);
        }
        
        // Export to JSON
        function exportToJSON() {
            const dataStr = JSON.stringify(accountsData, null, 2);
            const dataBlob = new Blob([dataStr], {type: 'application/json'});
            const url = URL.createObjectURL(dataBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'instagram_results_' + new Date().getTime() + '.json';
            link.click();
            URL.revokeObjectURL(url);
            showCopyNotification('تم تصدير JSON بنجاح');
        }
        
        // Export to CSV
        function exportToCSV() {
            let csv = 'اسم المستخدم,الحالة,الاسم الكامل,المتابعون,المتابَعون,المنشورات,موثق,خاص,نوع الحساب,تاريخ الانضمام,آخر نشاط\n';
            
            accountsData.forEach(acc => {
                const info = acc.account_info || {};
                csv += `"${acc.username}",`;
                csv += `"${acc.status}",`;
                csv += `"${info.full_name || ''}",`;
                csv += `"${info.followers_count || 0}",`;
                csv += `"${info.following_count || 0}",`;
                csv += `"${info.posts_count || 0}",`;
                csv += `"${info.is_verified ? 'نعم' : 'لا'}",`;
                csv += `"${info.is_private ? 'نعم' : 'لا'}",`;
                csv += `"${info.account_type || 'Personal'}",`;
                csv += `"${info.registration_date || ''}",`;
                csv += `"${info.last_post_date || ''}"\n`;
            });
            
            // Add BOM for Arabic support
            const BOM = '\uFEFF';
            const csvBlob = new Blob([BOM + csv], {type: 'text/csv;charset=utf-8;'});
            const url = URL.createObjectURL(csvBlob);
            const link = document.createElement('a');
            link.href = url;
            link.download = 'instagram_results_' + new Date().getTime() + '.csv';
            link.click();
            URL.revokeObjectURL(url);
            showCopyNotification('تم تصدير CSV بنجاح');
        }
        
        // Print results
        function printResults() {
            window.print();
        }
        
        // Show advanced statistics modal
        function showStatisticsModal() {
            const totalAccounts = accountsData.length;
            const availableAccounts = accountsData.filter(acc => acc.status === 'available');
            const takenAccounts = accountsData.filter(acc => acc.status === 'taken');
            const verifiedAccounts = accountsData.filter(acc => acc.account_info?.is_verified);
            const businessAccounts = accountsData.filter(acc => acc.account_info?.is_business_account);
            const privateAccounts = accountsData.filter(acc => acc.account_info?.is_private);
            
            let totalFollowers = 0;
            let totalFollowing = 0;
            let totalPosts = 0;
            let accountsWithData = 0;
            
            takenAccounts.forEach(acc => {
                if (acc.account_info) {
                    totalFollowers += acc.account_info.followers_count || 0;
                    totalFollowing += acc.account_info.following_count || 0;
                    totalPosts += acc.account_info.posts_count || 0;
                    accountsWithData++;
                }
            });
            
            const avgFollowers = accountsWithData > 0 ? Math.round(totalFollowers / accountsWithData) : 0;
            const avgFollowing = accountsWithData > 0 ? Math.round(totalFollowing / accountsWithData) : 0;
            const avgPosts = accountsWithData > 0 ? Math.round(totalPosts / accountsWithData) : 0;
            
            const statsHTML = `
                <div class="info-section">
                    <h3><i class="fas fa-chart-bar"></i> نظرة عامة</h3>
                    <div class="info-grid">
                        ${createInfoItem('إجمالي الحسابات', totalAccounts + ' 👥')}
                        ${createInfoItem('الحسابات المتاحة', availableAccounts.length + ' 🟢')}
                        ${createInfoItem('الحسابات المحجوزة', takenAccounts.length + ' 🔴')}
                        ${createInfoItem('نسبة التوفر', ((availableAccounts.length / totalAccounts) * 100).toFixed(1) + '% 📊')}
                    </div>
                </div>
                
                <div class="info-section">
                    <h3><i class="fas fa-shield-alt"></i> حالة الحسابات</h3>
                    <div class="info-grid">
                        ${createInfoItem('الحسابات الموثقة', verifiedAccounts.length + ' ✓')}
                        ${createInfoItem('حسابات الأعمال', businessAccounts.length + ' 💼')}
                        ${createInfoItem('الحسابات الخاصة', privateAccounts.length + ' 🔒')}
                        ${createInfoItem('الحسابات العامة', (takenAccounts.length - privateAccounts.length) + ' 🌐')}
                    </div>
                </div>
                
                <div class="info-section">
                    <h3><i class="fas fa-calculator"></i> المتوسطات</h3>
                    <div class="info-grid">
                        ${createInfoItem('متوسط المتابعين', formatNumber(avgFollowers) + ' 👥')}
                        ${createInfoItem('متوسط المتابَعين', formatNumber(avgFollowing) + ' 👤')}
                        ${createInfoItem('متوسط المنشورات', formatNumber(avgPosts) + ' 📸')}
                        ${createInfoItem('إجمالي المتابعين', formatNumber(totalFollowers) + ' 🌟')}
                    </div>
                </div>
                
                <div class="info-section">
                    <h3><i class="fas fa-trophy"></i> أعلى الحسابات</h3>
                    <div class="info-grid">
                        ${getTopAccount('followers', '👑 أكثر متابعين')}
                        ${getTopAccount('posts', '📸 أكثر منشورات')}
                    </div>
                </div>
            `;
            
            const modalBody = document.getElementById('modalBody');
            modalBody.innerHTML = statsHTML;
            
            document.getElementById('modalUsername').innerHTML = '<i class="fas fa-chart-pie"></i> إحصائيات متقدمة';
            document.getElementById('modalFullName').textContent = 'تحليل شامل لنتائج البحث';
            
            // Hide profile pic in modal
            const modalProfilePicContainer = document.getElementById('modalProfilePic').parentElement;
            modalProfilePicContainer.innerHTML = '<div class="modal-profile-pic-placeholder"><i class="fas fa-chart-line"></i></div>';
            
            document.getElementById('accountModal').classList.add('active');
        }
        
        // Show Charts Modal
        function showChartsModal() {
            const takenAccounts = accountsData.filter(acc => acc.status === 'taken' && acc.account_info);
            
            if (takenAccounts.length === 0) {
                showCopyNotification('لا توجد بيانات كافية لعرض الرسوم البيانية');
                return;
            }
            
            // Prepare data for charts
            const sortedByFollowers = [...takenAccounts]
                .sort((a, b) => (b.account_info.followers_count || 0) - (a.account_info.followers_count || 0))
                .slice(0, 10);
            
            const sortedByPosts = [...takenAccounts]
                .sort((a, b) => (b.account_info.posts_count || 0) - (a.account_info.posts_count || 0))
                .slice(0, 10);
            
            const statsHTML = `
                <div class="info-section">
                    <h3><i class="fas fa-chart-line"></i> الرسوم البيانية التفاعلية</h3>
                    
                    <div class="chart-container">
                        <div class="chart-title">🏆 أعلى 10 حسابات بالمتابعين</div>
                        <canvas id="followersChart"></canvas>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">📸 أعلى 10 حسابات بالمنشورات</div>
                        <canvas id="postsChart"></canvas>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">📊 توزيع أنواع الحسابات</div>
                        <canvas id="accountTypesChart"></canvas>
                    </div>
                    
                    <div class="chart-container">
                        <div class="chart-title">🔄 نسبة المتاح/المحجوز</div>
                        <canvas id="statusChart"></canvas>
                    </div>
                </div>
            `;
            
            const modalBody = document.getElementById('modalBody');
            modalBody.innerHTML = statsHTML;
            
            document.getElementById('modalUsername').innerHTML = '<i class="fas fa-chart-line"></i> الرسوم البيانية';
            document.getElementById('modalFullName').textContent = 'تصور مرئي للبيانات';
            
            const modalProfilePicContainer = document.getElementById('modalProfilePic').parentElement;
            modalProfilePicContainer.innerHTML = '<div class="modal-profile-pic-placeholder"><i class="fas fa-chart-area"></i></div>';
            
            document.getElementById('accountModal').classList.add('active');
            
            // Create charts after modal is visible
            setTimeout(() => {
                createFollowersChart(sortedByFollowers);
                createPostsChart(sortedByPosts);
                createAccountTypesChart();
                createStatusChart();
            }, 100);
        }
        
        // Create Followers Chart
        function createFollowersChart(data) {
            const ctx = document.getElementById('followersChart');
            if (!ctx) return;
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(acc => '@' + acc.username),
                    datasets: [{
                        label: 'المتابعون',
                        data: data.map(acc => acc.account_info.followers_count || 0),
                        backgroundColor: 'rgba(131, 58, 180, 0.6)',
                        borderColor: 'rgba(131, 58, 180, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true,
                            ticks: {
                                callback: function(value) {
                                    return formatNumber(value);
                                }
                            }
                        }
                    }
                }
            });
        }
        
        // Create Posts Chart
        function createPostsChart(data) {
            const ctx = document.getElementById('postsChart');
            if (!ctx) return;
            
            new Chart(ctx, {
                type: 'bar',
                data: {
                    labels: data.map(acc => '@' + acc.username),
                    datasets: [{
                        label: 'المنشورات',
                        data: data.map(acc => acc.account_info.posts_count || 0),
                        backgroundColor: 'rgba(225, 48, 108, 0.6)',
                        borderColor: 'rgba(225, 48, 108, 1)',
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            display: false
                        }
                    },
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        }
        
        // Create Account Types Chart
        function createAccountTypesChart() {
            const ctx = document.getElementById('accountTypesChart');
            if (!ctx) return;
            
            const personal = accountsData.filter(acc => acc.account_info?.account_type === 'Personal').length;
            const business = accountsData.filter(acc => acc.account_info?.account_type === 'Business').length;
            const professional = accountsData.filter(acc => acc.account_info?.account_type === 'Professional').length;
            
            new Chart(ctx, {
                type: 'doughnut',
                data: {
                    labels: ['شخصي', 'أعمال', 'احترافي'],
                    datasets: [{
                        data: [personal, business, professional],
                        backgroundColor: [
                            'rgba(131, 58, 180, 0.8)',
                            'rgba(225, 48, 108, 0.8)',
                            'rgba(253, 29, 29, 0.8)'
                        ],
                        borderColor: [
                            'rgba(131, 58, 180, 1)',
                            'rgba(225, 48, 108, 1)',
                            'rgba(253, 29, 29, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
        
        // Create Status Chart
        function createStatusChart() {
            const ctx = document.getElementById('statusChart');
            if (!ctx) return;
            
            const available = accountsData.filter(acc => acc.status === 'available').length;
            const taken = accountsData.filter(acc => acc.status === 'taken').length;
            
            new Chart(ctx, {
                type: 'pie',
                data: {
                    labels: ['متاح', 'محجوز'],
                    datasets: [{
                        data: [available, taken],
                        backgroundColor: [
                            'rgba(0, 200, 83, 0.8)',
                            'rgba(225, 48, 108, 0.8)'
                        ],
                        borderColor: [
                            'rgba(0, 200, 83, 1)',
                            'rgba(225, 48, 108, 1)'
                        ],
                        borderWidth: 2
                    }]
                },
                options: {
                    responsive: true,
                    maintainAspectRatio: false,
                    plugins: {
                        legend: {
                            position: 'bottom'
                        }
                    }
                }
            });
        }
        
        // Get top account by metric
        function getTopAccount(metric, label) {
            let topAccount = null;
            let maxValue = 0;
            
            accountsData.forEach(acc => {
                if (acc.account_info) {
                    let value = 0;
                    if (metric === 'followers') value = acc.account_info.followers_count || 0;
                    else if (metric === 'posts') value = acc.account_info.posts_count || 0;
                    
                    if (value > maxValue) {
                        maxValue = value;
                        topAccount = acc;
                    }
                }
            });
            
            if (topAccount) {
                return createInfoItem(label, `@${topAccount.username} (${formatNumber(maxValue)})`);
            }
            return createInfoItem(label, 'لا توجد بيانات');
        }
        
        // Compare Accounts
        function compareAccounts() {
            const takenAccounts = accountsData.filter(acc => acc.status === 'taken' && acc.account_info);
            
            if (takenAccounts.length < 2) {
                showCopyNotification('يجب وجود حسابين محجوزين على الأقل للمقارنة');
                return;
            }
            
            // Get top 2 accounts by followers
            const top2 = [...takenAccounts]
                .sort((a, b) => (b.account_info.followers_count || 0) - (a.account_info.followers_count || 0))
                .slice(0, 2);
            
            const acc1 = top2[0];
            const acc2 = top2[1];
            
            const comparisonHTML = `
                <div class="info-section">
                    <h3><i class="fas fa-balance-scale"></i> مقارنة بين أعلى حسابين</h3>
                    
                    <div class="comparison-grid">
                        <div class="comparison-card">
                            <h4>@${acc1.username}</h4>
                            ${createInfoItem('الاسم الكامل', acc1.account_info.full_name || '-')}
                            ${createInfoItem('المتابعون', formatNumber(acc1.account_info.followers_count || 0) + ' 👥')}
                            ${createInfoItem('المتابَعون', formatNumber(acc1.account_info.following_count || 0) + ' 👤')}
                            ${createInfoItem('المنشورات', formatNumber(acc1.account_info.posts_count || 0) + ' 📸')}
                            ${createInfoItem('موثق', acc1.account_info.is_verified ? 'نعم ✓' : 'لا ✗')}
                            ${createInfoItem('نوع الحساب', acc1.account_info.account_type || 'Personal')}
                            ${createInfoItem('خاص', acc1.account_info.is_private ? 'نعم 🔒' : 'لا 🌐')}
                        </div>
                        
                        <div style="text-align: center; display: flex; align-items: center; justify-content: center;">
                            <div class="vs-badge">VS</div>
                        </div>
                        
                        <div class="comparison-card">
                            <h4>@${acc2.username}</h4>
                            ${createInfoItem('الاسم الكامل', acc2.account_info.full_name || '-')}
                            ${createInfoItem('المتابعون', formatNumber(acc2.account_info.followers_count || 0) + ' 👥')}
                            ${createInfoItem('المتابَعون', formatNumber(acc2.account_info.following_count || 0) + ' 👤')}
                            ${createInfoItem('المنشورات', formatNumber(acc2.account_info.posts_count || 0) + ' 📸')}
                            ${createInfoItem('موثق', acc2.account_info.is_verified ? 'نعم ✓' : 'لا ✗')}
                            ${createInfoItem('نوع الحساب', acc2.account_info.account_type || 'Personal')}
                            ${createInfoItem('خاص', acc2.account_info.is_private ? 'نعم 🔒' : 'لا 🌐')}
                        </div>
                    </div>
                    
                    <div class="info-section" style="margin-top: 30px;">
                        <h3><i class="fas fa-chart-bar"></i> مقارنة الإحصائيات</h3>
                        <div class="chart-container">
                            <canvas id="comparisonChart"></canvas>
                        </div>
                    </div>
                    
                    <div class="info-section">
                        <h3><i class="fas fa-trophy"></i> النتيجة</h3>
                        <div class="info-grid">
                            ${createInfoItem('الأكثر متابعين', 
                                (acc1.account_info.followers_count || 0) > (acc2.account_info.followers_count || 0) ? 
                                '@' + acc1.username + ' 🏆' : '@' + acc2.username + ' 🏆')}
                            ${createInfoItem('الأكثر نشاطاً', 
                                (acc1.account_info.posts_count || 0) > (acc2.account_info.posts_count || 0) ? 
                                '@' + acc1.username + ' 📸' : '@' + acc2.username + ' 📸')}
                        </div>
                    </div>
                </div>
            `;
            
            const modalBody = document.getElementById('modalBody');
            modalBody.innerHTML = comparisonHTML;
            
            document.getElementById('modalUsername').innerHTML = '<i class="fas fa-balance-scale"></i> مقارنة الحسابات';
            document.getElementById('modalFullName').textContent = 'مقارنة تفصيلية بين أعلى حسابين';
            
            const modalProfilePicContainer = document.getElementById('modalProfilePic').parentElement;
            modalProfilePicContainer.innerHTML = '<div class="modal-profile-pic-placeholder"><i class="fas fa-users"></i></div>';
            
            document.getElementById('accountModal').classList.add('active');
            
            // Create comparison chart
            setTimeout(() => {
                const ctx = document.getElementById('comparisonChart');
                if (ctx) {
                    new Chart(ctx, {
                        type: 'radar',
                        data: {
                            labels: ['المتابعون', 'المتابَعون', 'المنشورات'],
                            datasets: [
                                {
                                    label: '@' + acc1.username,
                                    data: [
                                        Math.min((acc1.account_info.followers_count || 0) / 1000, 100),
                                        Math.min((acc1.account_info.following_count || 0) / 100, 100),
                                        Math.min((acc1.account_info.posts_count || 0) / 10, 100)
                                    ],
                                    backgroundColor: 'rgba(131, 58, 180, 0.2)',
                                    borderColor: 'rgba(131, 58, 180, 1)',
                                    borderWidth: 2
                                },
                                {
                                    label: '@' + acc2.username,
                                    data: [
                                        Math.min((acc2.account_info.followers_count || 0) / 1000, 100),
                                        Math.min((acc2.account_info.following_count || 0) / 100, 100),
                                        Math.min((acc2.account_info.posts_count || 0) / 10, 100)
                                    ],
                                    backgroundColor: 'rgba(225, 48, 108, 0.2)',
                                    borderColor: 'rgba(225, 48, 108, 1)',
                                    borderWidth: 2
                                }
                            ]
                        },
                        options: {
                            responsive: true,
                            maintainAspectRatio: false,
                            scales: {
                                r: {
                                    beginAtZero: true,
                                    max: 100
                                }
                            }
                        }
                    });
                }
            }, 100);
        }
    </script>
</body>
</html>'''
    
    @staticmethod
    def create_html_report(accounts_data: List[Dict], filename: str = None) -> str:
        """إنشاء تقرير HTML من بيانات الحسابات مع ملف JSON منفصل"""
        try:
            # Determine filenames
            if not filename:
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                html_filename = f'instagram_results_{timestamp}.html'
                json_filename = 'data.json'
            else:
                html_filename = filename
                # JSON file in same directory
                json_filename = 'data.json'
            
            # Clean data before JSON conversion
            clean_data = []
            for account in accounts_data:
                clean_account = {
                    'username': account.get('username', ''),
                    'status': account.get('status', 'unknown'),
                    'checked_at': account.get('checked_at', ''),
                    'account_info': account.get('account_info')
                }
                clean_data.append(clean_account)
            
            # Save JSON file
            json_path = os.path.join(os.path.dirname(html_filename) if os.path.dirname(html_filename) else '.', json_filename)
            try:
                with open(json_path, 'w', encoding='utf-8') as f:
                    json.dump(clean_data, f, ensure_ascii=False, indent=2)
                print(f"{Colors.OKGREEN}✓ تم حفظ ملف JSON: {json_path}{Colors.ENDC}")
                print(f"{Colors.OKGREEN}✓ تم تحويل {len(clean_data)} حساب إلى JSON{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.FAIL}❌ خطأ في حفظ ملف JSON: {str(e)}{Colors.ENDC}")
                raise
            
            # Get HTML template (without data injection)
            html_content = HTMLExporter.get_html_template()
            
            # Save HTML file
            try:
                with open(html_filename, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                print(f"{Colors.OKGREEN}✓ تم حفظ ملف HTML: {html_filename}{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.FAIL}❌ خطأ في حفظ ملف HTML: {str(e)}{Colors.ENDC}")
                raise
            
            print(f"{Colors.OKBLUE}💡 ملاحظة: ملف HTML يقرأ البيانات من {json_filename}{Colors.ENDC}")
            print(f"{Colors.WARNING}⚠️  احذر: إذا حذفت {json_filename} لن تظهر البيانات في HTML{Colors.ENDC}")
            
            return html_filename
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ خطأ في إنشاء التقرير: {str(e)}{Colors.ENDC}")
            raise

class InstagramHunter:
    def __init__(self, save_directory: str = None):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Instagram 269.0.0.18.75 Android (30/11; 420dpi; 1080x2260; samsung; SM-G973F; beyond1; exynos9820; ar_IQ; 314665256)',
            'Accept': '*/*',
            'Accept-Language': 'ar-IQ,ar;q=0.9,en-US;q=0.8,en;q=0.7',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
            'X-IG-App-ID': '936619743392459',
            'X-IG-WWW-Claim': '0',
        })
        
        # تحديد مجلد الحفظ
        if save_directory:
            self.save_directory = save_directory
        else:
            self.save_directory = os.path.dirname(os.path.abspath(__file__))
        
        # إنشاء مجلد للنتائج إذا لم يكن موجوداً
        self.results_dir = os.path.join(self.save_directory, 'instagram_results')
        os.makedirs(self.results_dir, exist_ok=True)
        
        # User agents للتنويع
        self.user_agents = [
            'Instagram 269.0.0.18.75 Android (30/11; 420dpi; 1080x2260; samsung; SM-G973F; beyond1; exynos9820; ar_IQ; 314665256)',
            'Instagram 275.0.0.27.98 Android (31/12; 480dpi; 1080x2400; xiaomi; M2102J20SG; alioth; qcom; ar_IQ; 460920956)',
            'Instagram 280.0.0.24.109 Android (32/13; 560dpi; 1440x3040; samsung; SM-N975F; d2s; exynos9825; ar_IQ; 478267672)',
        ]
        
        # إحصائيات البحث
        self.search_stats = {
            'total_checked': 0,
            'available': 0,
            'taken': 0,
            'unknown': 0,
            'start_time': None,
            'end_time': None
        }
        
        # HTML results file path
        self.html_results_file = os.path.join(self.results_dir, 'instagram_all_results.html')
        
        # Load existing HTML data if exists
        self.all_accounts_data = []
        self._load_existing_html_data()
    
    def _load_existing_html_data(self):
        """تحميل البيانات من ملف HTML الموجود"""
        if os.path.exists(self.html_results_file):
            try:
                with open(self.html_results_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                    # Extract JSON data from HTML
                    start_marker = 'const accountsData = '
                    end_marker = ';\n'
                    start_idx = content.find(start_marker)
                    if start_idx != -1:
                        start_idx += len(start_marker)
                        end_idx = content.find(end_marker, start_idx)
                        if end_idx != -1:
                            json_data = content[start_idx:end_idx]
                            self.all_accounts_data = json.loads(json_data)
                            print(f"{Colors.OKGREEN}✓ تم تحميل {len(self.all_accounts_data)} حساب من الملف الموجود{Colors.ENDC}")
            except Exception as e:
                print(f"{Colors.WARNING}⚠️ تعذر تحميل البيانات الموجودة: {str(e)}{Colors.ENDC}")
    
    def _get_random_user_agent(self) -> str:
        """الحصول على User Agent عشوائي"""
        return random.choice(self.user_agents)
    
    def _make_request(self, url: str, method: str = 'GET', **kwargs) -> Optional[requests.Response]:
        """إرسال طلب HTTP مع معالجة الأخطاء"""
        try:
            self.session.headers['User-Agent'] = self._get_random_user_agent()
            
            if method.upper() == 'GET':
                response = self.session.get(url, timeout=15, **kwargs)
            else:
                response = self.session.post(url, timeout=15, **kwargs)
            
            time.sleep(random.uniform(0.5, 2))
            
            return response
        except Exception as e:
            return None
    
    def check_username_availability(self, username: str) -> Tuple[str, Optional[Dict]]:
        """
        التحقق من توفر اسم المستخدم
        Returns: (status, data) حيث status = 'available', 'taken', 'unknown'
        """
        url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}'
        
        response = self._make_request(url)
        
        if not response:
            return 'unknown', None
        
        if response.status_code == 404:
            return 'available', None
        elif response.status_code == 200:
            try:
                return 'taken', response.json()
            except:
                return 'unknown', None
        else:
            return 'unknown', None
    
    def get_account_detailed_info(self, username: str, silent: bool = False) -> Optional[AccountInfo]:
        """جلب معلومات مفصلة عن الحساب"""
        if not silent:
            print(f"\n{Colors.OKCYAN}{'='*80}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}🔍 جاري جلب معلومات الحساب: @{username}{Colors.ENDC}")
            print(f"{Colors.OKCYAN}{'='*80}{Colors.ENDC}")
        
        account_info = self._get_profile_info(username, silent)
        
        if account_info:
            self._enrich_account_info(account_info, silent)
            self._calculate_engagement_rate(account_info)
            return account_info
        
        return None
    
    def _get_profile_info(self, username: str, silent: bool = False) -> Optional[AccountInfo]:
        """جلب المعلومات الأساسية للملف الشخصي"""
        url = f'https://www.instagram.com/api/v1/users/web_profile_info/?username={username}'
        
        response = self._make_request(url)
        
        if not response or response.status_code != 200:
            if not silent:
                print(f"{Colors.FAIL}❌ فشل جلب معلومات الحساب{Colors.ENDC}")
            return None
        
        try:
            data = response.json()
            user_data = data.get('data', {}).get('user', {})
            
            if not user_data:
                return None
            
            # استخراج تاريخ أول منشور لتقدير تاريخ الانضمام
            registration_date = None
            last_post_date = None
            
            # محاولة الحصول على تاريخ من المنشورات
            edge_posts = user_data.get('edge_owner_to_timeline_media', {})
            edges = edge_posts.get('edges', [])
            
            if edges:
                # آخر منشور
                if len(edges) > 0:
                    latest_timestamp = edges[0].get('node', {}).get('taken_at_timestamp')
                    if latest_timestamp:
                        last_post_date = datetime.fromtimestamp(latest_timestamp).strftime('%Y-%m-%d')
                
                # أول منشور (تقريب لتاريخ الانضمام)
                if len(edges) > 0:
                    # البحث عن أقدم منشور
                    oldest_timestamp = None
                    for edge in edges[-3:]:  # آخر 3 منشورات (الأقدم)
                        timestamp = edge.get('node', {}).get('taken_at_timestamp')
                        if timestamp:
                            if oldest_timestamp is None or timestamp < oldest_timestamp:
                                oldest_timestamp = timestamp
                    
                    if oldest_timestamp:
                        registration_date = datetime.fromtimestamp(oldest_timestamp).strftime('%Y-%m-%d')
            
            # تحديد إذا كان الحساب جديد
            is_joined_recently = user_data.get('is_joined_recently', False)
            
            # إذا كان منضم حديثاً ولا يوجد تاريخ
            if is_joined_recently and not registration_date:
                # تقدير: خلال الـ 6 أشهر الماضية
                from datetime import timedelta
                registration_date = (datetime.now() - timedelta(days=180)).strftime('%Y-%m-%d')
            
            account_info = AccountInfo(
                username=username,
                user_id=user_data.get('id'),
                full_name=user_data.get('full_name'),
                biography=user_data.get('biography'),
                external_url=user_data.get('external_url'),
                is_private=user_data.get('is_private', False),
                is_verified=user_data.get('is_verified', False),
                profile_pic_url=user_data.get('profile_pic_url_hd') or user_data.get('profile_pic_url'),
                followers_count=user_data.get('edge_followed_by', {}).get('count', 0),
                following_count=user_data.get('edge_follow', {}).get('count', 0),
                posts_count=user_data.get('edge_owner_to_timeline_media', {}).get('count', 0),
                is_business_account=user_data.get('is_business_account', False),
                is_professional_account=user_data.get('is_professional_account', False),
                business_category_name=user_data.get('business_category_name'),
                category_name=user_data.get('category_name'),
                has_highlight_reels=user_data.get('highlight_reel_count', 0) > 0,
                highlight_reel_count=user_data.get('highlight_reel_count', 0),
                is_joined_recently=is_joined_recently,
                registration_date=registration_date,
                last_post_date=last_post_date,
                availability_status='taken',
                public_email=user_data.get('business_email'),
                public_phone_number=user_data.get('business_phone_number'),
            )
            
            # تحديد نوع الحساب
            if account_info.is_business_account:
                account_info.account_type = "Business"
            elif account_info.is_professional_account:
                account_info.account_type = "Professional"
            else:
                account_info.account_type = "Personal"
            
            # حساب معدل النشر التقريبي
            if account_info.posts_count > 0 and registration_date:
                try:
                    reg_date = datetime.strptime(registration_date, '%Y-%m-%d')
                    days_active = (datetime.now() - reg_date).days
                    if days_active > 0:
                        posts_per_day = account_info.posts_count / days_active
                        account_info.average_likes = int(posts_per_day * 100)  # تقدير
                except:
                    pass
            
            return account_info
            
        except Exception as e:
            if not silent:
                print(f"{Colors.FAIL}❌ خطأ في معالجة البيانات: {str(e)}{Colors.ENDC}")
            return None
    
    def _enrich_account_info(self, account_info: AccountInfo, silent: bool = False):
        """إثراء معلومات الحساب بمعلومات إضافية"""
        pass
    
    def _calculate_engagement_rate(self, account_info: AccountInfo):
        """حساب معدل التفاعل"""
        if account_info.followers_count > 0:
            total_engagement = account_info.average_likes + account_info.average_comments
            account_info.engagement_rate = (total_engagement / account_info.followers_count) * 100
    
    def print_account_info(self, account_info: AccountInfo):
        """طباعة معلومات الحساب بشكل جميل"""
        print(f"\n{Colors.OKGREEN}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}👤 معلومات الحساب التفصيلية{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'='*80}{Colors.ENDC}\n")
        
        print(f"{Colors.OKCYAN}📝 اسم المستخدم:{Colors.ENDC} @{account_info.username}")
        if account_info.full_name:
            print(f"{Colors.OKCYAN}👤 الاسم الكامل:{Colors.ENDC} {account_info.full_name}")
        if account_info.biography:
            print(f"{Colors.OKCYAN}📄 السيرة الذاتية:{Colors.ENDC} {account_info.biography}")
        
        print(f"\n{Colors.OKBLUE}📊 الإحصائيات:{Colors.ENDC}")
        print(f"  • المتابعون: {account_info.followers_count:,}")
        print(f"  • المتابَعون: {account_info.following_count:,}")
        print(f"  • المنشورات: {account_info.posts_count:,}")
        
        print(f"\n{Colors.OKBLUE}✨ حالة الحساب:{Colors.ENDC}")
        print(f"  • موثق: {'نعم ✓' if account_info.is_verified else 'لا'}")
        print(f"  • خاص: {'نعم' if account_info.is_private else 'لا'}")
        print(f"  • نوع الحساب: {account_info.account_type}")
        
        print(f"\n{Colors.OKGREEN}{'='*80}{Colors.ENDC}\n")
    
    def save_account_info_to_file(self, account_info: AccountInfo):
        """حفظ معلومات الحساب في ملف JSON"""
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = os.path.join(self.results_dir, f'account_{account_info.username}_{timestamp}.json')
        
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(asdict(account_info), f, ensure_ascii=False, indent=4)
            
            print(f"{Colors.OKGREEN}✓ تم حفظ البيانات في: {filename}{Colors.ENDC}")
        except Exception as e:
            print(f"{Colors.FAIL}❌ خطأ في الحفظ: {str(e)}{Colors.ENDC}")
    
    def search_rare_usernames(self, length: int = 3, count: int = 100, 
                             include_numbers: bool = False, include_dot: bool = False,
                             include_underscore: bool = False, mixed: bool = False,
                             max_time: Optional[int] = None) -> List[UsernameSearchResult]:
        """البحث عن أسماء مستخدمين نادرة"""
        print(f"\n{Colors.HEADER}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}🎯 بدء البحث عن اليوزرات النادرة{Colors.ENDC}")
        print(f"{Colors.HEADER}{'='*80}{Colors.ENDC}\n")
        
        print(f"{Colors.OKCYAN}⚙️ إعدادات البحث:{Colors.ENDC}")
        print(f"  • الطول: {length} حرف")
        print(f"  • العدد المطلوب: {count}")
        print(f"  • أرقام: {'نعم' if include_numbers else 'لا'}")
        print(f"  • نقطة: {'نعم' if include_dot else 'لا'}")
        print(f"  • شرطة سفلية: {'نعم' if include_underscore else 'لا'}")
        print(f"  • مختلط: {'نعم' if mixed else 'لا'}")
        if max_time:
            print(f"  • الحد الزمني: {max_time} ثانية")
        
        results = []
        checked = 0
        start_time = time.time()
        
        self.search_stats['start_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        print(f"\n{Colors.OKCYAN}{'='*80}{Colors.ENDC}")
        print(f"{Colors.OKCYAN}🔍 جاري البحث...{Colors.ENDC}")
        print(f"{Colors.OKCYAN}{'='*80}{Colors.ENDC}\n")
        
        while checked < count:
            # Check time limit
            if max_time and (time.time() - start_time) >= max_time:
                print(f"\n{Colors.WARNING}⏱️ تم الوصول إلى الحد الزمني ({max_time}s){Colors.ENDC}")
                break
            
            # Generate username
            username = self._generate_username(length, include_numbers, include_dot, 
                                              include_underscore, mixed)
            
            # Check availability
            status, data = self.check_username_availability(username)
            
            result = UsernameSearchResult(
                username=username,
                status=status
            )
            
            # If taken, get account info
            if status == 'taken':
                account_info = self.get_account_detailed_info(username, silent=True)
                result.account_info = account_info
            
            results.append(result)
            checked += 1
            
            # Update stats
            self.search_stats['total_checked'] += 1
            if status == 'available':
                self.search_stats['available'] += 1
                print(f"{Colors.OKGREEN}[{checked}/{count}] ✓ متاح: @{username}{Colors.ENDC}")
            elif status == 'taken':
                self.search_stats['taken'] += 1
                print(f"{Colors.FAIL}[{checked}/{count}] ✗ محجوز: @{username}{Colors.ENDC}")
            else:
                self.search_stats['unknown'] += 1
                print(f"{Colors.WARNING}[{checked}/{count}] ? غير معروف: @{username}{Colors.ENDC}")
        
        self.search_stats['end_time'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Print summary
        self._print_search_summary()
        
        return results
    
    def _generate_username(self, length: int, include_numbers: bool, 
                          include_dot: bool, include_underscore: bool, 
                          mixed: bool) -> str:
        """توليد اسم مستخدم عشوائي"""
        chars = string.ascii_lowercase
        
        if include_numbers or mixed:
            chars += string.digits
        
        username = ''.join(random.choices(chars, k=length))
        
        if include_dot and random.random() > 0.5:
            pos = random.randint(1, len(username)-1)
            username = username[:pos] + '.' + username[pos:]
        
        if include_underscore and random.random() > 0.5:
            pos = random.randint(1, len(username)-1)
            username = username[:pos] + '_' + username[pos:]
        
        return username
    
    def _print_search_summary(self):
        """طباعة ملخص نتائج البحث"""
        print(f"\n{Colors.OKGREEN}{'='*80}{Colors.ENDC}")
        print(f"{Colors.OKGREEN}📊 ملخص البحث{Colors.ENDC}")
        print(f"{Colors.OKGREEN}{'='*80}{Colors.ENDC}\n")
        
        print(f"{Colors.OKCYAN}إجمالي المفحوص:{Colors.ENDC} {self.search_stats['total_checked']}")
        print(f"{Colors.OKGREEN}متاح:{Colors.ENDC} {self.search_stats['available']}")
        print(f"{Colors.FAIL}محجوز:{Colors.ENDC} {self.search_stats['taken']}")
        print(f"{Colors.WARNING}غير معروف:{Colors.ENDC} {self.search_stats['unknown']}")
        
        if self.search_stats['start_time'] and self.search_stats['end_time']:
            print(f"\n{Colors.OKCYAN}وقت البدء:{Colors.ENDC} {self.search_stats['start_time']}")
            print(f"{Colors.OKCYAN}وقت الانتهاء:{Colors.ENDC} {self.search_stats['end_time']}")
        
        print(f"\n{Colors.OKGREEN}{'='*80}{Colors.ENDC}\n")
    
    def save_search_results(self, results: List[UsernameSearchResult], 
                           search_type: str = "search"):
        """حفظ نتائج البحث في ملف HTML"""
        try:
            # Convert results to dict format
            accounts_data = []
            for result in results:
                account_dict = {
                    'username': result.username,
                    'status': result.status,
                    'checked_at': result.checked_at,
                    'account_info': asdict(result.account_info) if result.account_info else None
                }
                accounts_data.append(account_dict)
                
                # Check if account already exists in all_accounts_data
                existing_idx = None
                for idx, existing in enumerate(self.all_accounts_data):
                    if existing['username'] == result.username:
                        existing_idx = idx
                        break
                
                # Update or append
                if existing_idx is not None:
                    self.all_accounts_data[existing_idx] = account_dict
                else:
                    self.all_accounts_data.append(account_dict)
            
            # Create HTML file with all accumulated data
            html_file = HTMLExporter.create_html_report(
                self.all_accounts_data,
                self.html_results_file
            )
            
            # Also save JSON backup
            json_file = os.path.join(self.results_dir, f'{search_type}_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json')
            with open(json_file, 'w', encoding='utf-8') as f:
                json.dump(accounts_data, f, ensure_ascii=False, indent=2)
            
            print(f"\n{Colors.OKGREEN}{'='*80}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}✓ تم حفظ النتائج بنجاح!{Colors.ENDC}")
            print(f"{Colors.OKGREEN}{'='*80}{Colors.ENDC}\n")
            print(f"{Colors.OKCYAN}📄 ملف HTML:{Colors.ENDC} {html_file}")
            print(f"{Colors.OKCYAN}📄 ملف JSON:{Colors.ENDC} {json_file}")
            print(f"{Colors.OKCYAN}📊 إجمالي الحسابات في الملف:{Colors.ENDC} {len(self.all_accounts_data)}")
            print(f"\n{Colors.OKGREEN}{'='*80}{Colors.ENDC}\n")
            
        except Exception as e:
            print(f"{Colors.FAIL}❌ خطأ في حفظ النتائج: {str(e)}{Colors.ENDC}")

def print_banner():
    """طباعة شعار البرنامج"""
    banner = f"""{Colors.HEADER}
╔══════════════════════════════════════════════════════════════════════════════╗
║                                                                              ║
║              ██╗███╗   ██╗███████╗████████╗ █████╗  ██████╗ ██████╗         ║
║              ██║████╗  ██║██╔════╝╚══██╔══╝██╔══██╗██╔════╝ ██╔══██╗        ║
║              ██║██╔██╗ ██║███████╗   ██║   ███████║██║  ███╗██████╔╝        ║
║              ██║██║╚██╗██║╚════██║   ██║   ██╔══██║██║   ██║██╔══██╗        ║
║              ██║██║ ╚████║███████║   ██║   ██║  ██║╚██████╔╝██║  ██║        ║
║              ╚═╝╚═╝  ╚═══╝╚══════╝   ╚═╝   ╚═╝  ╚═╝ ╚═════╝ ╚═╝  ╚═╝        ║
║                                                                              ║
║                        🎯 Ultimate Hunter V4 🎯                              ║
║                     Professional Instagram Analysis Tool                     ║
║                         with HTML Export Feature                             ║
║                                                                              ║
║                    💻 Kraar - Digital Creativity Company                     ║
║                              🇮🇶 Iraq 🇮🇶                                      ║
║                                                                              ║
╚══════════════════════════════════════════════════════════════════════════════╝
{Colors.ENDC}"""
    print(banner)

def rare_username_search_menu(hunter: InstagramHunter):
    """قائمة البحث عن اليوزرات النادرة"""
    print(f"\n{Colors.OKBLUE}{'='*80}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}🎯 البحث عن اليوزرات النادرة{Colors.ENDC}")
    print(f"{Colors.OKBLUE}{'='*80}{Colors.ENDC}\n")
    
    # اختيار الطول
    print(f"{Colors.OKCYAN}📏 اختر طول الاسم:{Colors.ENDC}")
    print(f"{Colors.OKGREEN}[1]{Colors.ENDC} 3 أحرف (نادر جداً)")
    print(f"{Colors.OKGREEN}[2]{Colors.ENDC} 4 أحرف (نادر)")
    print(f"{Colors.OKGREEN}[3]{Colors.ENDC} 5 أحرف (متوسط)")
    print(f"{Colors.OKGREEN}[4]{Colors.ENDC} 6 أحرف")
    print(f"{Colors.OKGREEN}[5]{Colors.ENDC} 7+ أحرف")
    print(f"{Colors.OKGREEN}[6]{Colors.ENDC} طول مخصص")
    
    length_choice = input(f"\n{Colors.OKCYAN}➤ اختر (1-6): {Colors.ENDC}").strip()
    
    length_map = {
        '1': 3,
        '2': 4,
        '3': 5,
        '4': 6,
        '5': 7
    }
    
    if length_choice in length_map:
        length = length_map[length_choice]
    elif length_choice == '6':
        try:
            length = int(input(f"{Colors.OKCYAN}➤ أدخل الطول المطلوب (1-30): {Colors.ENDC}").strip())
            if length < 1 or length > 30:
                print(f"{Colors.FAIL}❌ الطول يجب أن يكون بين 1-30{Colors.ENDC}")
                return
        except:
            print(f"{Colors.FAIL}❌ إدخال غير صحيح{Colors.ENDC}")
            return
    else:
        print(f"{Colors.FAIL}❌ اختيار غير صحيح{Colors.ENDC}")
        return
    
    # عدد الأسماء
    try:
        count = int(input(f"\n{Colors.OKCYAN}📊 كم اسم تريد فحصه؟ (مثال: 100): {Colors.ENDC}").strip())
        if count < 1:
            print(f"{Colors.FAIL}❌ يجب أن يكون العدد أكبر من 0{Colors.ENDC}")
            return
    except:
        print(f"{Colors.FAIL}❌ إدخال غير صحيح{Colors.ENDC}")
        return
    
    # الخيارات المتقدمة
    print(f"\n{Colors.OKCYAN}⚙️ الخيارات المتقدمة:{Colors.ENDC}")
    
    include_numbers = input(f"{Colors.OKCYAN}➤ تضمين أرقام؟ (y/n): {Colors.ENDC}").strip().lower() == 'y'
    include_dot = input(f"{Colors.OKCYAN}➤ تضمين نقطة (.)؟ (y/n): {Colors.ENDC}").strip().lower() == 'y'
    include_underscore = input(f"{Colors.OKCYAN}➤ تضمين شرطة (_)؟ (y/n): {Colors.ENDC}").strip().lower() == 'y'
    mixed = input(f"{Colors.OKCYAN}➤ مختلط (أحرف وأرقام)؟ (y/n): {Colors.ENDC}").strip().lower() == 'y'
    
    # حد زمني اختياري
    time_limit_input = input(f"\n{Colors.OKCYAN}⏱️ حد زمني للبحث بالثواني (اضغط Enter للتخطي): {Colors.ENDC}").strip()
    max_time = None
    if time_limit_input:
        try:
            max_time = int(time_limit_input)
        except:
            print(f"{Colors.WARNING}⚠️ تجاهل الحد الزمني (إدخال غير صحيح){Colors.ENDC}")
    
    # بدء البحث
    results = hunter.search_rare_usernames(
        length=length,
        count=count,
        include_numbers=include_numbers,
        include_dot=include_dot,
        include_underscore=include_underscore,
        mixed=mixed,
        max_time=max_time
    )
    
    # حفظ النتائج تلقائياً في HTML
    if results:
        hunter.save_search_results(results, search_type=f"rare_{length}char")
        
        # عرض اليوزرات المتاحة
        available_usernames = [r for r in results if r.status == 'available']
        if available_usernames:
            print(f"\n{Colors.OKGREEN}{'='*80}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}✅ اليوزرات المتاحة ({len(available_usernames)}):{Colors.ENDC}")
            print(f"{Colors.OKGREEN}{'='*80}{Colors.ENDC}\n")
            
            for i, result in enumerate(available_usernames, 1):
                print(f"{Colors.OKGREEN}[{i}] @{result.username}{Colors.ENDC}")

def main_menu():
    """القائمة الرئيسية"""
    hunter = InstagramHunter()
    
    print_banner()
    print(f"\n{Colors.OKGREEN}مرحباً بك في Instagram Ultimate Hunter V4!{Colors.ENDC}")
    print(f"{Colors.OKCYAN}أداة احترافية شاملة لتحليل حسابات Instagram والبحث عن اليوزرات النادرة{Colors.ENDC}")
    print(f"{Colors.WARNING}📁 مجلد النتائج: {hunter.results_dir}{Colors.ENDC}")
    print(f"{Colors.WARNING}📄 ملف HTML الرئيسي: {hunter.html_results_file}{Colors.ENDC}\n")
    
    while True:
        print(f"\n{Colors.OKBLUE}{'='*80}{Colors.ENDC}")
        print(f"{Colors.HEADER}{Colors.BOLD}📋 القائمة الرئيسية:{Colors.ENDC}")
        print(f"{Colors.OKBLUE}{'='*80}{Colors.ENDC}\n")
        
        print(f"{Colors.OKGREEN}[1]{Colors.ENDC} 🔍 البحث التفصيلي عن حساب واحد")
        print(f"{Colors.OKGREEN}[2]{Colors.ENDC} 📋 البحث عن عدة حسابات دفعة واحدة")
        print(f"{Colors.OKGREEN}[3]{Colors.ENDC} ✅ التحقق من توفر اسم مستخدم")
        print(f"{Colors.OKGREEN}[4]{Colors.ENDC} 💾 البحث والحفظ المباشر")
        print(f"{Colors.OKGREEN}[5]{Colors.ENDC} 🎯 البحث عن اليوزرات النادرة (جديد!)")
        print(f"{Colors.OKGREEN}[6]{Colors.ENDC} 📂 عرض الملفات المحفوظة")
        print(f"{Colors.OKGREEN}[7]{Colors.ENDC} 🌐 فتح ملف HTML الرئيسي")
        print(f"{Colors.OKGREEN}[0]{Colors.ENDC} 🚪 خروج")
        
        choice = input(f"\n{Colors.OKCYAN}➤ اختر خياراً (0-7): {Colors.ENDC}").strip()
        
        if choice == '1':
            # البحث عن حساب واحد
            username = input(f"\n{Colors.OKCYAN}📝 أدخل اسم المستخدم (بدون @): {Colors.ENDC}").strip().replace('@', '')
            
            if username:
                account_info = hunter.get_account_detailed_info(username)
                
                if account_info:
                    hunter.print_account_info(account_info)
                    
                    save = input(f"\n{Colors.OKCYAN}💾 هل تريد حفظ هذه البيانات في HTML؟ (y/n): {Colors.ENDC}").strip().lower()
                    if save == 'y':
                        # Create result object
                        result = UsernameSearchResult(
                            username=username,
                            status='taken',
                            account_info=account_info
                        )
                        hunter.save_search_results([result], search_type="single_search")
                else:
                    print(f"\n{Colors.FAIL}❌ لم نتمكن من جلب معلومات الحساب @{username}{Colors.ENDC}")
        
        elif choice == '2':
            # البحث عن عدة حسابات
            print(f"\n{Colors.OKCYAN}📝 أدخل أسماء المستخدمين (كل اسم في سطر منفصل){Colors.ENDC}")
            print(f"{Colors.WARNING}   اضغط Enter مرتين للانتهاء{Colors.ENDC}\n")
            
            usernames = []
            while True:
                username = input(f"{Colors.OKCYAN}➤ {Colors.ENDC}").strip().replace('@', '')
                if not username:
                    break
                usernames.append(username)
            
            if usernames:
                results = []
                for username in usernames:
                    account_info = hunter.get_account_detailed_info(username, silent=True)
                    if account_info:
                        result = UsernameSearchResult(
                            username=username,
                            status='taken',
                            account_info=account_info
                        )
                        results.append(result)
                        hunter.print_account_info(account_info)
                
                if results:
                    save = input(f"\n{Colors.OKCYAN}💾 حفظ جميع النتائج في HTML؟ (y/n): {Colors.ENDC}").strip().lower()
                    if save == 'y':
                        hunter.save_search_results(results, search_type="bulk_search")
        
        elif choice == '3':
            # التحقق من توفر اسم
            username = input(f"\n{Colors.OKCYAN}📝 أدخل اسم المستخدم (بدون @): {Colors.ENDC}").strip().replace('@', '')
            
            if username:
                status, data = hunter.check_username_availability(username)
                
                if status == 'available':
                    print(f"\n{Colors.OKGREEN}✅ اسم المستخدم @{username} متاح!{Colors.ENDC}")
                    
                    save = input(f"{Colors.OKCYAN}💾 حفظ في HTML؟ (y/n): {Colors.ENDC}").strip().lower()
                    if save == 'y':
                        result = UsernameSearchResult(username=username, status='available')
                        hunter.save_search_results([result], search_type="availability_check")
                        
                elif status == 'taken':
                    print(f"\n{Colors.FAIL}❌ اسم المستخدم @{username} محجوز{Colors.ENDC}")
                    
                    view = input(f"{Colors.OKCYAN}🔍 عرض معلومات الحساب؟ (y/n): {Colors.ENDC}").strip().lower()
                    if view == 'y':
                        account_info = hunter.get_account_detailed_info(username)
                        if account_info:
                            hunter.print_account_info(account_info)
                            
                            save = input(f"\n{Colors.OKCYAN}💾 حفظ في HTML؟ (y/n): {Colors.ENDC}").strip().lower()
                            if save == 'y':
                                result = UsernameSearchResult(
                                    username=username,
                                    status='taken',
                                    account_info=account_info
                                )
                                hunter.save_search_results([result], search_type="availability_check")
                else:
                    print(f"\n{Colors.WARNING}⚠️ حالة غير معروفة{Colors.ENDC}")
        
        elif choice == '4':
            # البحث والحفظ المباشر
            username = input(f"\n{Colors.OKCYAN}📝 أدخل اسم المستخدم (بدون @): {Colors.ENDC}").strip().replace('@', '')
            
            if username:
                account_info = hunter.get_account_detailed_info(username)
                if account_info:
                    result = UsernameSearchResult(
                        username=username,
                        status='taken',
                        account_info=account_info
                    )
                    hunter.save_search_results([result], search_type="direct_save")
        
        elif choice == '5':
            # البحث عن اليوزرات النادرة
            rare_username_search_menu(hunter)
        
        elif choice == '6':
            # عرض الملفات المحفوظة
            try:
                files = os.listdir(hunter.results_dir)
                html_files = [f for f in files if f.endswith('.html')]
                json_files = [f for f in files if f.endswith('.json')]
                
                if html_files or json_files:
                    print(f"\n{Colors.OKGREEN}📂 الملفات المحفوظة:{Colors.ENDC}\n")
                    
                    if html_files:
                        print(f"{Colors.OKCYAN}📄 ملفات HTML ({len(html_files)}):{Colors.ENDC}")
                        for i, file in enumerate(html_files, 1):
                            file_path = os.path.join(hunter.results_dir, file)
                            size = os.path.getsize(file_path)
                            print(f"  [{i}] {file} ({size:,} بايت)")
                    
                    if json_files:
                        print(f"\n{Colors.OKCYAN}📄 ملفات JSON ({len(json_files)}):{Colors.ENDC}")
                        for i, file in enumerate(json_files, 1):
                            file_path = os.path.join(hunter.results_dir, file)
                            size = os.path.getsize(file_path)
                            print(f"  [{i}] {file} ({size:,} بايت)")
                else:
                    print(f"\n{Colors.WARNING}⚠️ لا توجد ملفات محفوظة{Colors.ENDC}")
            except Exception as e:
                print(f"\n{Colors.FAIL}❌ خطأ: {str(e)}{Colors.ENDC}")
        
        elif choice == '7':
            # فتح ملف HTML الرئيسي
            if os.path.exists(hunter.html_results_file):
                print(f"\n{Colors.OKGREEN}🌐 ملف HTML الرئيسي:{Colors.ENDC} {hunter.html_results_file}")
                print(f"{Colors.OKCYAN}📊 عدد الحسابات:{Colors.ENDC} {len(hunter.all_accounts_data)}")
                
                # Try to open in browser
                try:
                    import webbrowser
                    webbrowser.open('file://' + os.path.abspath(hunter.html_results_file))
                    print(f"{Colors.OKGREEN}✓ تم فتح الملف في المتصفح{Colors.ENDC}")
                except:
                    print(f"{Colors.WARNING}⚠️ يمكنك فتح الملف يدوياً من المسار أعلاه{Colors.ENDC}")
            else:
                print(f"\n{Colors.WARNING}⚠️ لا يوجد ملف HTML محفوظ بعد{Colors.ENDC}")
                print(f"{Colors.OKCYAN}قم بإجراء بحث أولاً لإنشاء الملف{Colors.ENDC}")
        
        elif choice == '0':
            print(f"\n{Colors.OKGREEN}{'='*80}{Colors.ENDC}")
            print(f"{Colors.OKGREEN}👋 شكراً لاستخدامك Instagram Ultimate Hunter V4!{Colors.ENDC}")
            print(f"{Colors.OKCYAN}   Kraar - Digital Creativity Company - Iraq 🇮🇶{Colors.ENDC}")
            print(f"{Colors.OKGREEN}{'='*80}{Colors.ENDC}\n")
            break
        
        else:
            print(f"\n{Colors.FAIL}❌ خيار غير صحيح{Colors.ENDC}")

if __name__ == '__main__':
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n\n{Colors.WARNING}⚠️ تم إيقاف البرنامج{Colors.ENDC}\n")
    except Exception as e:
        print(f"\n{Colors.FAIL}❌ خطأ غير متوقع: {str(e)}{Colors.ENDC}\n")