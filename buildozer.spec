
[app]
title = Galleons
package.name = galleons
package.domain = org.galleons
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 1.0

# Requirements (Add android for AdMob)
requirements = python3,kivy,requests,android,jnius

# Android config
orientation = portrait
fullscreen = 1
android.api = 31
android.minapi = 21
android.ndk = 25b  # Required for Android 12+

# Permissions (Add WAKE_LOCK for ads)
android.permissions = INTERNET, ACCESS_NETWORK_STATE, WAKE_LOCK

# AdMob Metadata (CRITICAL)
android.meta_data = com.google.android.gms.ads.APPLICATION_ID=ca-app-pub-6179277409535855~6192143253

# Gradle dependencies (For AdMob)
android.gradle_dependencies =
    implementation 'com.google.android.gms:play-services-ads:22.6.0'

# Icons
icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/presplash.png

# Packaging
package.unique = 1

[buildozer]
log_level = 2
warn_on_root = 1
