---
title: Introduction
description: Get started with OpenSees.
date: 2024-08-14
aliases:
  - "/docs/getting-started/"
  - "/getting-started/"
  - "/docs/"
layout: docs
---

## Installation

In order to install `xara` run the command:

{{< command >}}
python -m pip install xara
{{< /command >}}

## Running OpenSees

The `xara` package can be used in three ways:

{{< accordion class="accordion-theme accordion-flush" >}}
  {{< accordion-item header="Python Module" >}}
    The `opensees.openseespy` Python module implements the API that has been developed by Oregon State.
  {{< /accordion-item >}}
  {{< accordion-item header="Command line interface" >}}
    An interactive Tcl interpreter can be started by invoking the module as follows from the command line:
    {{< command >}}
    python -m opensees --help
    {{< /command >}}
  {{< /accordion-item >}}
  {{< accordion-item header="Interactive Interpreter" >}}
    An interactive Tcl interpreter can be started by invoking the module as follows from the command line:
    {{< command >}}
    python -m opensees
    {{< /command >}}

  {{< /accordion-item >}}
{{< /accordion >}}


