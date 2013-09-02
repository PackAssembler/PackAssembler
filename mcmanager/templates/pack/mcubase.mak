<?xml version="1.0" encoding="UTF-8"?>
<ServerPack version="3.0" xmlns:noNamespaceSchemaLocation="http://www.mcupdater.com/ServerPack"
    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
    xsi:schemaLocation="http://www.mcupdater.com/ServerPack ServerPackv2.xsd ">
    <Server id="mcubase" name="MCU3 1.6.2" newsUrl="http://mcupdater.com"
        revision="1" serverAddress="localhost" version="${mc_version}"
        mainClass="net.minecraft.launchwrapper.Launch">
        <Module id="forge" name="Minecraft Forge">
            <URL>http://files.minecraftforge.net/minecraftforge/minecraftforge-universal-${mc_version}-${forge_version}.jar</URL>
            <Required>true</Required>
            <ModType order="1"
                launchArgs="--tweakClass cpw.mods.fml.common.launcher.FMLTweaker">Library</ModType>
            <Submodule id="launchwrapper" name="Mojang (LaunchWrapper)">
                <URL>https://s3.amazonaws.com/Minecraft.Download/libraries/net/minecraft/launchwrapper/1.5/launchwrapper-1.5.jar</URL>
                <Required>true</Required>
                <ModType order="3">Library</ModType>
            </Submodule>
            <Submodule id="asm" name="Mojang (ASM)">
                <URL>https://s3.amazonaws.com/Minecraft.Download/libraries/org/ow2/asm/asm-all/4.1/asm-all-4.1.jar</URL>
                <Required>true</Required>
                <ModType order="3">Library</ModType>
            </Submodule>
            <Submodule id="scala-lib" name="Minecraft Forge (scala-library)">
                <URL>http://files.minecraftforge.net/maven/org/scala-lang/scala-library/2.10.2/scala-library-2.10.2.jar</URL>
                <Required>true</Required>
                <ModType order="4">Library</ModType>
            </Submodule>
            <Submodule id="scala-compiler" name="Minecraft Forge (scala-compiler)">
                <URL>http://files.minecraftforge.net/maven/org/scala-lang/scala-compiler/2.10.2/scala-compiler-2.10.2.jar</URL>
                <Required>true</Required>
                <ModType order="5">Library</ModType>
            </Submodule>
            <Submodule id="lzma" name="Mojang (LZMA)">
                <URL>https://s3.amazonaws.com/Minecraft.Download/libraries/lzma/lzma/0.0.1/lzma-0.0.1.jar</URL>
                <Required>true</Required>
                <ModType order="6">Library</ModType>
            </Submodule>
        </Module>
    </Server>
</ServerPack>
