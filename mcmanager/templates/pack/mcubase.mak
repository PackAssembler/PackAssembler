<?xml version="1.0" encoding="UTF-8"?>
<ServerPack version="3.0" xmlns:noNamespaceSchemaLocation="http://www.mcupdater.com/ServerPack"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="https://raw.github.com/MCUpdater/MCUpdater/develop/MCU-API/ServerPackv2.xsd">
    <Server id="mcubase" name="MCU3 1.6.2" newsUrl="http://mcupdater.com"
        revision="1" serverAddress="localhost" version="${mc_version}"
        mainClass="net.minecraft.launchwrapper.Launch">
        <Module id="forge" name="Minecraft Forge">
            <URL>http://files.minecraftforge.net/minecraftforge/minecraftforge-universal-${mc_version}-${forge_version}.jar</URL>
            <Required>true</Required>
            <ModType order="1"
                launchArgs="--tweakClass cpw.mods.fml.common.launcher.FMLTweaker">Library</ModType>
            <MD5></MD5>
            <Submodule id="launchwrapper" name="Mojang (LaunchWrapper)">
                <URL>https://s3.amazonaws.com/Minecraft.Download/libraries/net/minecraft/launchwrapper/1.5/launchwrapper-1.5.jar</URL>
                <Required>true</Required>
                <ModType order="3">Library</ModType>
                <MD5>a211ab7001fca1bc2b534a0a5847aed6</MD5>
            </Submodule>
            <Submodule id="asm" name="Mojang (ASM)">
                <URL>https://s3.amazonaws.com/Minecraft.Download/libraries/org/ow2/asm/asm-all/4.1/asm-all-4.1.jar</URL>
                <Required>true</Required>
                <ModType order="3">Library</ModType>
                <MD5>d21c2a06a4e6b175aa01e328f38a1182</MD5>
            </Submodule>
            <Submodule id="scala-lib" name="Minecraft Forge (scala-library)">
                <URL>http://files.minecraftforge.net/maven/org/scala-lang/scala-library/2.10.2/scala-library-2.10.2.jar</URL>
                <Required>true</Required>
                <ModType order="4">Library</ModType>
                <MD5>8800aafcc03e346dbbde171bef0b2bfe</MD5>
            </Submodule>
            <Submodule id="scala-compiler" name="Minecraft Forge (scala-compiler)">
                <URL>http://files.minecraftforge.net/maven/org/scala-lang/scala-compiler/2.10.2/scala-compiler-2.10.2.jar</URL>
                <Required>true</Required>
                <ModType order="5">Library</ModType>
                <MD5>44f4d11085423ebffbfb177c1fe4cc69</MD5>
            </Submodule>
            <Submodule id="lzma" name="Mojang (LZMA)">
                <URL>https://s3.amazonaws.com/Minecraft.Download/libraries/lzma/lzma/0.0.1/lzma-0.0.1.jar</URL>
                <Required>true</Required>
                <ModType order="6">Library</ModType>
                <MD5>a3e3c3186e41c4a1a3027ba2bb23cdc6</MD5>
            </Submodule>
        </Module>
    </Server>
</ServerPack>
