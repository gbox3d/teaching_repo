import java.util.jar.JarInputStream
import java.util.zip.ZipFile

plugins {
    id("com.android.library") version "9.2.1"
}

version = providers.gradleProperty("wlenoVersion").get()

android {
    namespace = "com.example.roomcontrol.wleno"
    compileSdk {
        version = release(36) { minorApiLevel = 1 }
    }
    defaultConfig {
        minSdk = 26
    }
    sourceSets {
        named("main") {
            kotlin.directories += "src"
            manifest.srcFile("AndroidManifest.xml")
        }
    }
    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
}

dependencies {
    api("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.9.0")
}

val aarName = "wleno-android-${project.version}.aar"
val releaseAar = layout.buildDirectory.file("outputs/aar/wleno-android-release.aar")
val distributionDirectory = layout.projectDirectory.dir("dist")

val copyReleaseAar by tasks.registering(Copy::class) {
    dependsOn("assembleRelease")
    doFirst {
        // A successful Gradle build can still produce an empty AAR when sources are misconfigured.
        ZipFile(releaseAar.get().asFile).use { aar ->
            val classes = aar.getEntry("classes.jar") ?: error("AAR has no classes.jar")
            val entries = aar.getInputStream(classes).use { input ->
                JarInputStream(input).use { jar ->
                    generateSequence { jar.nextJarEntry }.map { it.name }.toSet()
                }
            }
            for (name in listOf("Wleno", "WlenoClient", "ConnState", "SimulatorDevice", "WlenoMessage")) {
                check("com/example/roomcontrol/wleno/$name.class" in entries) {
                    "AAR is missing public API class: $name"
                }
            }
        }
    }
    from(releaseAar)
    into(distributionDirectory)
    rename { aarName }
}

tasks.register("packageDistribution") {
    dependsOn(copyReleaseAar)
    group = "distribution"
    description = "Build the classroom AAR for app/libs."
}
