<?php

use Twig\Environment;
use Twig\Error\LoaderError;
use Twig\Error\RuntimeError;
use Twig\Extension\SandboxExtension;
use Twig\Markup;
use Twig\Sandbox\SecurityError;
use Twig\Sandbox\SecurityNotAllowedTagError;
use Twig\Sandbox\SecurityNotAllowedFilterError;
use Twig\Sandbox\SecurityNotAllowedFunctionError;
use Twig\Source;
use Twig\Template;

/* index.twig */
class __TwigTemplate_165f90b97774943b792e86a8d3926015fa1a7ec64544337661973bde88aafb09 extends Template
{
    private $source;
    private $macros = [];

    public function __construct(Environment $env)
    {
        parent::__construct($env);

        $this->source = $this->getSourceContext();

        $this->blocks = [
            'content' => [$this, 'block_content'],
        ];
    }

    protected function doGetParent(array $context)
    {
        // line 1
        return "layouts/app.twig";
    }

    protected function doDisplay(array $context, array $blocks = [])
    {
        $macros = $this->macros;
        $this->parent = $this->loadTemplate("layouts/app.twig", "index.twig", 1);
        $this->parent->display($context, array_merge($this->blocks, $blocks));
    }

    // line 3
    public function block_content($context, array $blocks = [])
    {
        $macros = $this->macros;
        // line 4
        echo "    ";
        $this->loadTemplate("components/header.twig", "index.twig", 4)->display($context);
        // line 5
        echo "
    <div id=\"content\" class=\"flex flex-col flex-grow container mx-auto px-4 xl:max-w-screen-xl dark:text-white\">
        <div class=\"my-4\">
            <div class=\"flex justify-between font-bold p-4\">
                <div class=\"flex-grow font-mono mr-2\">
                    ";
        // line 10
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('translate')->getCallable(), ["file.name"]), "html", null, true);
        echo "
                </div>

                <div class=\"font-mono text-right w-1/6 mx-2 hidden sm:block\">
                    ";
        // line 14
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('translate')->getCallable(), ["file.size"]), "html", null, true);
        echo "
                </div>

                <div class=\"font-mono text-right w-1/4 ml-2 hidden sm:block\">
                    ";
        // line 18
        echo twig_escape_filter($this->env, call_user_func_array($this->env->getFunction('translate')->getCallable(), ["file.date"]), "html", null, true);
        echo "
                </div>
            </div>

            <ul id=\"file-list\">
                <li>
                    ";
        // line 24
        if ((($context["path"] ?? null) && (($context["path"] ?? null) != "."))) {
            // line 25
            echo "                        ";
            echo twig_include($this->env, $context, "components/file.twig", ["parentDir" => true]);
            echo "
                    ";
        }
        // line 27
        echo "                </li>

                <li>
                    ";
        // line 30
        $context['_parent'] = $context;
        $context['_seq'] = twig_ensure_traversable(($context["files"] ?? null));
        $context['loop'] = [
          'parent' => $context['_parent'],
          'index0' => 0,
          'index'  => 1,
          'first'  => true,
        ];
        if (is_array($context['_seq']) || (is_object($context['_seq']) && $context['_seq'] instanceof \Countable)) {
            $length = count($context['_seq']);
            $context['loop']['revindex0'] = $length - 1;
            $context['loop']['revindex'] = $length;
            $context['loop']['length'] = $length;
            $context['loop']['last'] = 1 === $length;
        }
        foreach ($context['_seq'] as $context["_key"] => $context["file"]) {
            // line 31
            echo "                        ";
            echo twig_include($this->env, $context, "components/file.twig");
            echo "
                    ";
            ++$context['loop']['index0'];
            ++$context['loop']['index'];
            $context['loop']['first'] = false;
            if (isset($context['loop']['length'])) {
                --$context['loop']['revindex0'];
                --$context['loop']['revindex'];
                $context['loop']['last'] = 0 === $context['loop']['revindex0'];
            }
        }
        $_parent = $context['_parent'];
        unset($context['_seq'], $context['_iterated'], $context['_key'], $context['file'], $context['_parent'], $context['loop']);
        $context = array_intersect_key($context, $_parent) + $_parent;
        // line 33
        echo "                </li>
            </ul>
        </div>

        ";
        // line 37
        if (($context["readme"] ?? null)) {
            // line 38
            echo "            ";
            $this->loadTemplate("components/readme.twig", "index.twig", 38)->display($context);
            // line 39
            echo "        ";
        }
        // line 40
        echo "    </div>

    ";
        // line 42
        $this->loadTemplate("components/footer.twig", "index.twig", 42)->display($context);
        // line 43
        echo "
    ";
        // line 44
        $this->loadTemplate("components/scroll-to-top.twig", "index.twig", 44)->display($context);
        // line 45
        echo "    <file-info-modal ref=\"fileInfoModal\"></file-info-modal>
";
    }

    public function getTemplateName()
    {
        return "index.twig";
    }

    public function isTraitable()
    {
        return false;
    }

    public function getDebugInfo()
    {
        return array (  155 => 45,  153 => 44,  150 => 43,  148 => 42,  144 => 40,  141 => 39,  138 => 38,  136 => 37,  130 => 33,  113 => 31,  96 => 30,  91 => 27,  85 => 25,  83 => 24,  74 => 18,  67 => 14,  60 => 10,  53 => 5,  50 => 4,  46 => 3,  35 => 1,);
    }

    public function getSourceContext()
    {
        return new Source("", "index.twig", "/var/www/directorylister/app/views/index.twig");
    }
}
