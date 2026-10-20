def main():
    from backend.library.platform_manager import PlatformManager

    manager = PlatformManager()

    platforms = manager.all_platforms()

    for platform in platforms:
        print(platform["id"], platform["name"], platform["type"])

    print()
    print("Emulador do PS2:", manager.emulator_for_platform("ps2"))

    print("Plugin do PS2:", manager.plugin_for_platform("ps2"))


if __name__ == "__main__":
    main()
